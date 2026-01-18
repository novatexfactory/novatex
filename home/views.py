from django.http import JsonResponse
from django.views.decorators.csrf import csrf_protect
from django.core import mail
from django.conf import settings
from django.core.mail.backends.smtp import EmailBackend
from django.core.mail import EmailMessage
import logging
from .models import ContactMessage
from .models import NewsletterSubscriber
from .utils import FormValidator
from .backends import ArvixeEmailBackend

# Configure logger for security and debugging
logger = logging.getLogger(__name__)

@csrf_protect
def subscribe_newsletter(request):
    if request.method == 'POST':
        raw_email = request.POST.get('email', '')
        
        # Используем наш централизованный валидатор
        is_valid, error_msg, cleaned_email = FormValidator.validate_subscription_data(raw_email)
        
        if not is_valid:
            return JsonResponse({'status': 'error', 'message': error_msg}, status=400)

        try:
            NewsletterSubscriber.objects.get_or_create(email=cleaned_email)
            return JsonResponse({'status': 'success'})
        except Exception as e:
            logger.error(f"Newsletter Error: {e}")
            return JsonResponse({'status': 'error'}, status=500)
            
    return JsonResponse({'status': 'invalid_method'}, status=405)
def contact_form_handler(request):
    if request.method == 'POST':
        # 1. Collect data
        data = {
            'name': request.POST.get('name'),
            'email': request.POST.get('email'),
            'phone': request.POST.get('phone'),
            'subject': request.POST.get('subject'),
            'message': request.POST.get('message'),
        }

        # 2. Use the imported Validator
        is_valid, error_msg, cleaned_data = FormValidator.validate_contact_data(data)
        
        if not is_valid:
            # Send friendly error to NovaTex Factory users
            return JsonResponse({'status': 'error', 'message': error_msg}, status=400)

        # 3. Save sanitized data (cleaned_data) to PostgreSQL
        ContactMessage.objects.create(**cleaned_data)
        return JsonResponse({'status': 'success'})
    
def contact_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        
        if all([name, email, phone, subject, message]):
            # 1. Save to Database (PostgreSQL)
            ContactMessage.objects.create(
                name=name, 
                email=email, 
                phone=phone,
                subject=subject,
                message=message
            )
            
            # 2. Send Email using the isolated Arvixe backend
            try:
                # Use the backend imported from .backends
                backend = ArvixeEmailBackend()

                email_obj = EmailMessage(
                    subject=f'NovaTex Contact: {subject}',
                    body=f'From: {name}\nPhone: {phone}\nEmail: {email}\n\n{message}',
                    from_email=settings.EMAIL_HOST_USER,
                    to=[settings.EMAIL_HOST_USER],
                    connection=backend
                )
                email_obj.send(fail_silently=False)
                print("Email sent successfully with ArvixeEmailBackend!")

            except Exception as e:
                logger.error(f"SMTP Error: {e}")
                print(f"SMTP Error: {e}")
            
            return JsonResponse({'status': 'success'})
            
    return JsonResponse({'status': 'error'})