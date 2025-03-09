from datetime import datetime, timedelta, timezone
from random import randint

from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views.generic import TemplateView, View, FormView, UpdateView

from posts.models import Post
from utils import send_sms_code
from .forms import UserRegistrationForm, LoginForm, EditProfileForm, MobileLoginForm, VerifyOtpCodeForm, \
    SendForgotPasswordSmsForm, ForgotPasswordForm
from .models import User, OtpCode


class UserLoginView(FormView):
    template_name = 'accounts/login.html'
    form_class = LoginForm

    def form_valid(self, form):
        user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
        if user is not None:
            login(self.request, user)
            messages.success(self.request, 'You are now logged in.', 'success')

            return redirect('accounts:profile', user.username)

        messages.error(self.request, 'Invalid username or password.', 'danger')
        return redirect('accounts:login')


class UserRegisterView(View):
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


class UserProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['user_information'] = User.objects.get(username=kwargs['username'])
        context['user_post'] = Post.objects.filter(author=context['user_information']).order_by('-created_at')
        context['unpublished_posts'] = context['user_post'].filter(is_published=False)

        return context


class UserLogoutView(LoginRequiredMixin, View):

    def get(self, request):
        logout(request)
        messages.success(request, 'You are now logged out.', 'success')

        return redirect('accounts:login')


class UserEditProfileView(LoginRequiredMixin, UpdateView):
    template_name = 'accounts/edit_profile.html'
    model = User
    form_class = EditProfileForm

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        if form.is_valid():
            messages.success(self.request, 'You are now edited successfully', extra_tags='success')
            form.save()
            return redirect('accounts:profile', self.request.user.username)


class UserLoginMobileView(View):
    template_name = 'mobile/login-mobile.html'
    form_class = MobileLoginForm

    def get(self, request):
        return render(request, self.template_name, {'form': self.form_class()})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            mobile = form.cleaned_data['mobile']
            mobile_in_database = User.objects.filter(phone_number=mobile).exists()
            if OtpCode.objects.filter(mobile=mobile).exists():
                messages.error(self.request, 'we sent you a code if you did not resave it please try 2 minute later',
                               'danger')
                return redirect('accounts:login_mobile')
            if mobile_in_database:
                random_number = randint(1000, 9999)
                OtpCode.objects.create(mobile=mobile, code=random_number)
                send_sms_code(mobile=mobile, code=random_number)
                request.session['user_login_data'] = {
                    'mobile': mobile,
                    'otp_code': random_number,
                }
                messages.success(self.request, 'The code sent to your mobile', 'success')
                return redirect('accounts:verify_otp')

            messages.error(self.request, 'invalid phone number or you have not registered yet!', 'danger')
            return redirect('accounts:login_mobile')
        return render(request, self.template_name, {'form': form})


class VerifyOtpCodeMobileView(View):
    template_name = 'mobile/verify_otp_code.html'
    from_class = VerifyOtpCodeForm

    def get(self, request):
        return render(request, self.template_name, {'form': self.from_class()})

    def post(self, request):
   
        form = self.from_class(request.POST)
        user_data = request.session.get('user_login_data')
        otp_code = OtpCode.objects.get(code=user_data['otp_code'])
        expire_otp_code = datetime.now(tz=timezone.utc) + timedelta(minutes=2)

        if form.is_valid():
            code = form.cleaned_data.get('code')
            if otp_code.code == code:
                if otp_code.created_at < expire_otp_code:
                    otp_code.delete()
                    messages.error(request, 'OTP code expired.', 'danger')
                    return redirect('accounts:login_mobile')
                user = User.objects.get(phone_number=user_data['mobile'])
                user.backend = 'django.contrib.auth.backends.ModelBackend'
                login(request, user)
                messages.success(request, 'You are now logged in', 'success')
                otp_code.delete()
                request.session['user_login_data'].clear()
                return redirect('accounts:profile', user.username)
            messages.success(request, 'Your otp code is invalid', 'danger')
            return redirect('accounts:verify_otp')
        return render(request, self.template_name, {'form': form})


class ForgotPasswordView(FormView):
    template_name = 'password/forgot-password.html'
    form_class = SendForgotPasswordSmsForm

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home:home')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        random_number = randint(1000, 9999)
        phone_number = form.cleaned_data['phone_number']
        user = User.objects.filter(phone_number=phone_number).exists()
        if not user:
            messages.error(self.request, 'This user is not exist !!!', 'danger')
            return redirect('accounts:forgot_password')
        else:
            OtpCode.objects.create(mobile=phone_number, code=random_number)
            send_sms_code(mobile=phone_number, code=random_number)
            self.request.session['forgot_password'] = {
                'phone': phone_number,
                'code': random_number,
            }
            messages.success(self.request, 'We sent you an Otp code', 'success')
            return redirect('accounts:password_reset')


class PasswordResetView(FormView):
    template_name = 'password/reset-password.html'
    form_class = ForgotPasswordForm

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home:home')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        user_forgot_password_info = self.request.session.get('forgot_password')
        verification_code = form.cleaned_data['verification_code']
        password = form.cleaned_data['new_password']

        otp_code = OtpCode.objects.filter(code=verification_code).exists()
        if not otp_code:
            messages.error(self.request, 'OTP code does not exist', 'danger')
            return redirect('accounts:password_reset')
        else:
            user = User.objects.get(phone_number=user_forgot_password_info['phone'])
            user.set_password(password)
            user.save()
            OtpCode.objects.filter(code=verification_code).delete()
            self.request.session['forgot_password'].clear()
            messages.success(self.request, 'Your password changed successfully', 'success')
        return redirect('accounts:login')
