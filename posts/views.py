from django.shortcuts import render
from django.views.generic import DetailView

from posts.models import Post


class PostDetailView(DetailView):
    template_name = 'posts/single_post.html'
    model = Post
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post'] = Post.objects.get(slug=self.kwargs['slug'])
        return context
