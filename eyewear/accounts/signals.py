from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from django.shortcuts import redirect

@receiver(user_logged_in)
def redirect_user_based_on_type(sender, user, request, **kwargs):
    if user.is_staff:
        request.session['redirect_url'] = '/admin/'
    else:
        request.session['redirect_url'] = 'index'
