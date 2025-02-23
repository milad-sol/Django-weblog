from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError

from .models import User


class UserCreationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ['full_name', 'username', 'phone_number', 'email']

    def clean_confirm_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if password and confirm_password and password != confirm_password:
            raise ValidationError('Passwords do not match')
        return confirm_password

    def clean_username(self):
        username = self.cleaned_data.get('username')
        user_in_database = User.objects.filter(username__iexact=username)
        if user_in_database:
            raise ValidationError('Username already exists')
        return username

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        phone_in_database = User.objects.filter(phone_number__iexact=phone_number)
        if phone_in_database:
            raise ValidationError('Phone number already exists')
        return phone_number

    def clean_email(self):
        email = self.cleaned_data.get('email')
        email_in_database = User.objects.filter(email__iexact=email)
        if email_in_database:
            raise ValidationError('Email already exists')
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data.get('password'))
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField(help_text="You can change password  <a href=\"../password/\">here</a>.")

    class Meta:
        model = User
        fields = ['phone_number', 'username', 'email', 'full_name', 'password', 'last_login']
