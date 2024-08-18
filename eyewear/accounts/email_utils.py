from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from .models import CustomUser

def send_registration_email(user):
    subject = 'Welcome to Our Site - Verify Your Email'
    from_email = settings.DEFAULT_FROM_EMAIL
    to = user.email
    text_content = 'This is an important message.'
    
    token = default_token_generator.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    verification_link = f"{settings.SITE_URL}/verify-email/{uid}/{token}/"
    
    html_content = render_to_string('registration_email.html', {
        'user': user.name,
        'verification_link': verification_link
    })
    
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()
