from django import forms

from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError
from .models import User, OtpCode


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
        user_in_database = User.objects.get(username__iexact=username)
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


# Create Register form

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Enter your Password'}))
    confirm_password = forms.CharField(label='Password confirmation',
                                       widget=forms.PasswordInput(
                                           attrs={'class': 'form-control',
                                                  'placeholder': 'Enter your Confirm Password'}))

    class Meta:
        model = User
        fields = ['full_name', 'username', 'phone_number', 'email', 'password', 'confirm_password']
        widgets = {

            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your Email'}),
            'full_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your Full Name'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your Phone Number'}),
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your Username'}),

        }

    def clean_confirm_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if password and confirm_password and password != confirm_password:
            raise ValidationError('Passwords do not match')
        return confirm_password

    def clean_email(self):
        email = self.cleaned_data.get('email')
        email_in_database = User.objects.filter(email__iexact=email)
        if email_in_database:
            raise ValidationError('Email already exists')
        return email

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        phone_number_in_database = User.objects.filter(phone_number__iexact=phone_number)
        if phone_number_in_database:
            raise ValidationError('Phone number already exists')
        return phone_number

    def clean_username(self):
        username = self.cleaned_data.get('username')
        user_in_database = User.objects.filter(username__iexact=username)
        if user_in_database:
            raise ValidationError('Username already exists')
        return username

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data.get('password'))
        if commit:
            user.save()
        return user


class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your username or phone'}))
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter your password'}))


class EditProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['bio', 'user_profile_image']
        widgets = {
            'bio': forms.Textarea(
                attrs={'class': 'form-control', 'placeholder': 'Tell us about yourself...', 'rows': 3, 'id': "bio",
                       }),
            'user_profile_image': ''
        }


class MobileLoginForm(forms.Form):
    mobile = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your mobile number'}))


class VerifyOtpCodeForm(forms.Form):
    code = forms.IntegerField(label='',
                              widget=forms.TextInput(
                                  attrs={'class': 'form-control', 'placeholder': 'Enter the code sent to your mobile'}))
