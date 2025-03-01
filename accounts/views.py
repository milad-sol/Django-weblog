from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views.generic import TemplateView, View, FormView, UpdateView
from posts.models import Post
from .forms import UserRegistrationForm, LoginForm, EditProfileForm
from .models import User
from django.contrib.auth import login, logout, authenticate
from django.urls import reverse


# Create your views here.


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
