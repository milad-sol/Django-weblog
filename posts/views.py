from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.utils.text import slugify
from django.views.generic import DetailView, TemplateView, CreateView, View

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
