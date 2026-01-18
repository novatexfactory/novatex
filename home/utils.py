import re
import logging
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.utils.html import strip_tags

# Configure logger for security and debugging
logger = logging.getLogger(__name__)

class FormValidator:
    """
    Utility class to centralize form validation and data sanitization
    to prevent XSS and ensure data integrity.
    """
    
    @staticmethod
    def validate_contact_data(data):
        """
        Sanitizes input and checks for required fields and valid formats.
        Returns: (is_valid, error_message, cleaned_data)
        """
        # 1. SANITIZATION (XSS Protection): Remove HTML tags from all inputs.
        # This keeps the text but prevents script injection.
        cleaned_data = {
            key: strip_tags(str(val)).strip() if val else "" 
            for key, val in data.items()
        }
        
        # 2. REQUIRED FIELDS: Basic check to ensure no field is empty.
        required_fields = ['name', 'email', 'phone', 'message']
        for field in required_fields:
            if not cleaned_data.get(field):
                return False, f"The field '{field}' is required.", None

        # 3. EMAIL VALIDATION: Ensure the email follows standard formats.
        try:
            validate_email(cleaned_data['email'])
        except ValidationError:
            logger.warning(f"Validation Error: Invalid email format ({cleaned_data['email']})")
            return False, "Please provide a valid email address.", None

        # 4. PHONE VALIDATION: Ensure it contains a reasonable number of digits.
        phone_digits = re.sub(r'\D', '', cleaned_data['phone'])
        if len(phone_digits) < 7 or len(phone_digits) > 15:
            return False, "Phone number should be between 7 and 15 digits.", None

        # 5. LENGTH VALIDATION: Prevent spam or database bloat.
        if len(cleaned_data['message']) < 10:
            return False, "Message is too short (minimum 10 characters).", None
        if len(cleaned_data['message']) > 3000:
            logger.critical(f"Spam Alert: Blocked long message from {cleaned_data['email']}")
            return False, "Message exceeds maximum allowed length.", None

        return True, None, cleaned_data
    
    @staticmethod
    def validate_subscription_data(email):
        """
        Validates only the email field for the footer newsletter.
        Returns: (is_valid, error_message, cleaned_email)
        """
        if not email:
            return False, "Email is required.", None
        
        cleaned_email = strip_tags(str(email)).strip()
        
        try:
            validate_email(cleaned_email)
            return True, None, cleaned_email
        except ValidationError:
            logger.warning(f"Subscription failed: Invalid email format ({cleaned_email})")
            return False, "Please provide a valid email address.", None