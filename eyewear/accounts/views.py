from django.shortcuts import render, redirect
from django.views import View
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from .serializers import RegisterSerializer, LoginSerializer
from .models import CustomUser
from django.contrib.auth import login,logout
from .email_utils import send_registration_email
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from django.contrib.auth.tokens import default_token_generator
from .models import CustomUser



class RegisterView(View):
    def get(self, request):
        return render(request, 'register.html')

    def post(self, request):
        data = request.POST
        serializer = RegisterSerializer(data=data)
        if serializer.is_valid():
            user = serializer.save()
            user.is_active = False  # Deactivate until email is verified
            user.save()
            send_registration_email(user)
            return redirect('login')
        return render(request, 'register.html', {'errors': serializer.errors})

class LoginView(View):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        serializer = LoginSerializer(data=request.POST)
        if serializer.is_valid():
            user = serializer.validated_data
            login(request, user)  # Log in the user
            token, created = Token.objects.get_or_create(user=user)
            if user.is_staff:
                return redirect('/admin/')
            else:
                return redirect('index') 
        # print(f"Login errors: {serializer.errors}")  # Debug statement to check login errors
        return render(request, 'login.html', {'errors': serializer.errors})


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('login')


class VerifyEmailView(View):
    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = CustomUser.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            return redirect('login')
        else:
            return render(request, 'email_verification_failed.html')

class IndexView(View):
    def get(self, request):
        return render(request, 'index.html')



class IndexView(View):
    def get(self, request):
        return render(request, 'index.html')

class ProductsView(View):
    def get(self, request):
        return render(request, 'products.html')

class AboutView(View):
    def get(self, request):
        return render(request, 'about.html')

class BlogsView(View):
    def get(self, request):
        return render(request, 'blogs.html')

class ContactView(View):
    def get(self, request):
        return render(request, 'contact.html')


class CartView(View):
    def get(self, request):
        return render(request, 'cart.html')


