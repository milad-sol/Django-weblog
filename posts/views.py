from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.utils.text import slugify
from django.views.generic import DetailView, CreateView, DeleteView, UpdateView, View

from .forms import CreatePostForm
from posts.models import Post, Category


class PostDetailView(DetailView):
    template_name = 'posts/single_post.html'
    model = Post
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post'] = Post.objects.get(slug=self.kwargs['slug'])
        return context


class CreatePostView(LoginRequiredMixin, CreateView):
    template_name = 'posts/create_new_post.html'
    model = Post
    form_class = CreatePostForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, 'Post created successfully', 'success')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('accounts:profile', kwargs={'username': self.request.user.username})


class PostDeleteView(LoginRequiredMixin, DeleteView):
    template_name = 'posts/delete_post.html'
    model = Post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post'] = Post.objects.get(slug=self.kwargs['slug'])
        return context

    def dispatch(self, request, *args, **kwargs):
        user = request.user
        post = Post.objects.get(slug=self.kwargs['slug'])
        if post.author != user:
            messages.error(request, f'You are not authorized to delete this post.this post belongs to {post.author}',
                           'danger')
            return redirect('accounts:profile', request.user.username)
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('accounts:profile', kwargs={'username': self.request.user.username})


class PostUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'posts/update_post.html'
    model = Post
    form_class = CreatePostForm

    def dispatch(self, request, *args, **kwargs):
        user = request.user
        post = Post.objects.get(slug=self.kwargs['slug'])
        if post.author != user:
            messages.error(request, 'You are not authorized to edit this post.', 'danger')
            return redirect('accounts:profile', user.username)
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, 'Post updated successfully', 'success')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('accounts:profile', kwargs={'username': self.request.user.username})
