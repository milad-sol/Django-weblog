from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import DetailView, CreateView, DeleteView, UpdateView, ListView, TemplateView, View
from .forms import CreatePostForm, CommentCreateForm, CommentReplyForm
from posts.models import Post, Category, Comment


class PostDetailView(View):
    template_name = 'posts/detail_post.html'

    context_object_name = 'post'
    comment_form = CommentCreateForm
    reply_form = CommentReplyForm

    def setup(self, request, *args, **kwargs):
        """
        because we need it in all method so we use setup
        """

        self.post_instance = get_object_or_404(Post, slug=kwargs['slug'])
        return super().setup(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        comments = Comment.objects.filter(post=self.post_instance, is_reply=False)
        return render(request, self.template_name,
                      context={'post': self.post_instance, 'comments': comments, 'comment_form': self.comment_form,
                               'reply_form': self.reply_form})

    """
    method_decorator is a function (actually a class acting as a decorator factory) in Django used to convert a function-based decorator into a method-based decorator. This is important when you want to apply decorators to methods within Django class-based views.
The Problem:
Regular function decorators don't work directly on methods of class-based views because the decorator receives the function itself, not the method bound to an instance. This loses the crucial self argument, preventing the method from accessing the view's instance and its attributes.
The Solution:
method_decorator solves this by creating a wrapper that correctly handles the self argument when the decorated method is called.
    """

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        form = self.comment_form(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.author = request.user
            new_comment.post = self.post_instance
            new_comment.save()
            messages.success(request, 'Your comment submitted successfully', extra_tags='success')
        return redirect('posts:post-detail', slug=kwargs['slug'])


class PostReplyCommentView(LoginRequiredMixin, View):
    form_class = CommentReplyForm

    def post(self, request, *args, **kwargs):
        post = get_object_or_404(Post, id=kwargs['post_id'])
        comment = get_object_or_404(Comment, id=kwargs['comment_id'])
        form = self.form_class(request.POST)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.author = request.user
            reply.post = post
            reply.parent = comment
            reply.is_reply = True
            reply.save()
            messages.success(request, 'Your reply submitted successfully', extra_tags='success')

        return redirect('posts:post-detail', slug=post.slug)


class CreatePostView(LoginRequiredMixin, CreateView):
    template_name = 'posts/create_new_post.html'
    model = Post
    form_class = CreatePostForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, 'Post created successfully', 'success')
        return super().form_valid(form)

    def get_success_url(self):
        messages.success(self.request, 'Post created successfully', 'success')
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
        messages.success(self.request, 'Post deleted successfully', 'success')
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


class PostCategoryListView(ListView):
    template_name = 'category/categories.html'
    model = Category
    context_object_name = 'categories'


class PostCategoryDetailView(DetailView):
    template_name = 'category/single_category.html'
    model = Category
    context_object_name = 'category'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = Category.objects.get(slug=self.kwargs['slug'])
        context['posts'] = Post.objects.filter(categories=context['category'])
        return context
