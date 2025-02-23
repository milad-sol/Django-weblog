from django.shortcuts import render
from django.views.generic import TemplateView


# Create your views here.
class RegisterView(TemplateView):
    template_name = 'accounts/register.html'


class LoginView(TemplateView):
    template_name = 'accounts/login.html'
