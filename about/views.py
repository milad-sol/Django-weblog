from django.shortcuts import render
from django.views.generic import TemplateView

from about.models import About


# Create your views here.
class AboutView(TemplateView):
    template_name = 'about/about.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['about'] = About.objects.first()
        return context
