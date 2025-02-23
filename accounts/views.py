from django.contrib import messages
from django.shortcuts import render, redirect
from django.views.generic import TemplateView, View, FormView
from .forms import UserRegistrationForm
from .models import User


# Create your views here.


class LoginView(TemplateView):
    template_name = 'accounts/login.html'


class RegisterView(View):
    template_name = 'accounts/register.html'
    class_form = UserRegistrationForm

    def get(self, request):
        return render(request, self.template_name, {'form': self.class_form()})

    def post(self, request):
        form = self.class_form(request.POST)
        if form.is_valid():
            User.objects.create_user(username=form.cleaned_data.get('username'),
                                     full_name=form.cleaned_data.get('full_name'),
                                     email=form.cleaned_data.get('email'), password=form.cleaned_data.get('password'),
                                     phone_number=form.cleaned_data.get('phone_number'))
            messages.success(request, 'Account created successfully', extra_tags='success')
            return redirect('accounts:login')
        messages.error(request, form.errors, extra_tags='danger')
        return render(request, self.template_name, {'form': form})
