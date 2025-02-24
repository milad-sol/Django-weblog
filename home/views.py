from django.views.generic import TemplateView, ListView
from posts.models import Post
from .models import WeblogSettings


class HomeView(TemplateView):
    template_name = 'home/home.html'  # Ensure this matches the template file name
    model = Post, WeblogSettings

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['settings'] = WeblogSettings.objects.first()
        context['features_posts'] = Post.objects.filter(feature_post=True)
        context['other_posts'] = Post.objects.filter(feature_post=False)
        return context
