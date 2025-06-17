# core/views.py
from django.shortcuts import render

def home(request):
    return render(request, 'index.html')

# Basic login/logout for now (Django's built-in views handle most)
from django.contrib.auth.views import LoginView, LogoutView

class CustomLoginView(LoginView):
    template_name = 'registration/login.html'
class CustomLogoutView(LogoutView):
    next_page = '/' # Redirect to home after logout