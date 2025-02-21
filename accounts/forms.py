from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError

from .models import User


class UserCreationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    password2 = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ['phone_number', 'email', 'full_name', 'password', 'password2']

    def clean_password2(self):
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')
        if password and password2 and password != password2:
            raise ValidationError('Passwords do not match')
        return password2

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        phone_number_in_database = User.objects.get(phone_number=phone_number)
        if phone_number_in_database == phone_number:
            raise ValidationError('Phone number already exists')
        return phone_number

    def clean_email(self):
        email = self.cleaned_data.get('email')
        email_in_database = User.objects.get(email=email)
        if email_in_database == email:
            raise ValidationError('Email already exists')
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data.get('password'))
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ['phone_number', 'email', 'full_name', 'password', 'is_active', 'is_admin','is_superuser']
