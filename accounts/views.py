from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views.generic import TemplateView, View, FormView, ListView

from posts.models import Post
from .forms import UserRegistrationForm, LoginForm
from .models import User
from django.contrib.auth import login, logout, authenticate


# Create your views here.


class LoginView(FormView):
    template_name = 'accounts/login.html'
    form_class = LoginForm
    model = User

    def form_valid(self, form):
        user_data = form.cleaned_data
        user = authenticate(username=user_data['username'], password=user_data['password'])
        if user is not None:
            print(user.id)
            login(self.request, user)
            messages.success(self.request, 'You are now logged in.', 'success')

            return redirect('accounts:profile', username=form.cleaned_data['username'])
        messages.error(self.request, 'Invalid username or password.', 'danger')
        return redirect('accounts:login')


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


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = User.objects.get(id=self.request.user.id)
        context['user_post'] = Post.objects.filter(author=self.request.user)
        return context
