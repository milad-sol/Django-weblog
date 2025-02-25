from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect, render

from django.urls import reverse_lazy
from django.utils.text import slugify
from django.views.decorators.http import require_safe
from django.views.generic import DetailView, TemplateView, CreateView, View, DeleteView

from posts.models import Post


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
    fields = ['title', 'content', 'image', 'categories']

    def form_valid(self, form):
        data = form.cleaned_data
        form.instance.author = self.request.user
        form.instance.slug = slugify(data['title'])
        return super().form_valid(form)


class PostDeleteView(LoginRequiredMixin, DeleteView):
    template_name = 'posts/delete_post.html'
    model = Post

    def dispatch(self, request, *args, **kwargs):
        user = request.user
        post = Post.objects.get(slug=self.kwargs['slug'])
        if post.author != user:
            messages.error(request,f'You are not authorized to delete this post.this post belongs to {post.author}', 'danger')
            return redirect('accounts:profile', request.user.username)
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('accounts:profile', kwargs={'username': self.request.user.username})
