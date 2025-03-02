from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views.generic import TemplateView, View, FormView, UpdateView
from posts.models import Post
from .forms import UserRegistrationForm, LoginForm, EditProfileForm, MobileLoginForm, VerifyOtpCodeForm
from .models import User, OtpCode
from django.contrib.auth import login, logout, authenticate
from random import randint
from utils import send_sms_code
from datetime import datetime, timedelta, timezone


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
        """
        Handles the POST request for OTP verification.

        This method retrieves the OTP code submitted by the user, compares it with the OTP code stored in the database,
        and logs the user in if the codes match.  It also handles form validation and error messages.

        Args:
            request (HttpRequest): The HTTP request object.

        Returns:
            HttpResponse:  A redirect to the user's profile page upon successful login, a redirect back to the OTP
                           verification page with an error message if the OTP is invalid, or a rendered form with errors
                           if the form validation fails.

        Note:
            `user.backend = 'django.contrib.auth.backends.ModelBackend'` is crucial for Django to
             correctly authenticate the user using the default model backend. Without this, Django might not
             be able to properly recognize the user as authenticated, especially when using custom authentication
             methods or backends initially.  This ensures that subsequent login attempts leverage the standard
             username/password verification process if needed, and that the user's permissions and groups are correctly
             loaded.
        """

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


