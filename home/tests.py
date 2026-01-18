from django.test import SimpleTestCase
from .utils import FormValidator

class ValidatorTest(SimpleTestCase):
    """
    Behavior-based tests for FormValidator to ensure security 
    and data integrity for NovaTex Factory.
    """

    def test_should_pass_validation_with_valid_data(self):
        """Should verify that correct data is accepted."""
        data = {
            'name': 'Evgeny Chauskey',
            'email': 'eugene@chauskey.com',
            'phone': '+1 469 388 3384',
            'message': 'Interested in Nixodine partnership.'
        }
        is_valid, error, cleaned = FormValidator.validate_contact_data(data)
        self.assertTrue(is_valid)
        self.assertIsNone(error)

    def test_should_strip_html_tags_to_prevent_xss(self):
        """Should ensure HTML tags are sanitized while keeping the text."""
        data = {
            'name': 'Hacker <script>alert("XSS")</script>',
            'email': 'hacker@test.com',
            'phone': '1234567890',
            'message': '<b>Danger message is here</b>' 
        }
        is_valid, error, cleaned = FormValidator.validate_contact_data(data)
        self.assertTrue(is_valid)
        self.assertNotIn('<script>', cleaned['name'])
        self.assertEqual(cleaned['message'], 'Danger message is here')

    def test_should_reject_malformed_email_address(self):
        """Should return an error message for invalid email formats."""
        data = {
            'name': 'Test',
            'email': 'not-an-email',
            'phone': '1234567890',
            'message': 'Valid message length'
        }
        is_valid, error, cleaned = FormValidator.validate_contact_data(data)
        self.assertFalse(is_valid)
        self.assertEqual(error, "Please provide a valid email address.")

    def test_should_reject_phone_numbers_outside_valid_range(self):
        """Should ensure phone numbers have between 7 and 15 digits."""
        data = {
            'name': 'Test',
            'email': 'test@test.com',
            'phone': '123',
            'message': 'Valid message length'
        }
        is_valid, error, cleaned = FormValidator.validate_contact_data(data)
        self.assertFalse(is_valid)
        self.assertIn("7 and 15 digits", error)

    def test_should_treat_sql_injection_as_plain_text(self):
        """Should sanitize SQL payloads to prevent database execution."""
        data = {
            'name': 'Attacker',
            'email': 'hacker@test.com',
            'phone': '1234567890',
            'message': "'; DROP TABLE home_contactmessage; -- Valid message length"
        }
        is_valid, error, cleaned = FormValidator.validate_contact_data(data)
        
        # Validated data stays safe; ORM will handle the text as a non-executable string.
        self.assertTrue(is_valid)
        self.assertIn("DROP TABLE", cleaned['message'])
        self.assertEqual(cleaned['name'], 'Attacker')

def test_should_reject_invalid_subscription_email(self):
        """Should verify that newsletter subscription also validates email."""
        invalid_email = "not-an-email-at-all"
        is_valid, error, cleaned = FormValidator.validate_subscription_data(invalid_email)
        self.assertFalse(is_valid)
        self.assertEqual(error, "Please provide a valid email address.")