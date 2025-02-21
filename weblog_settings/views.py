from django.shortcuts import render
from django.views.generic import DetailView, TemplateView

from weblog_settings.models import WeblogSettings


# Create your views here.
class WeblogSettingsView(TemplateView):
    template_name = 'weblog_settings/weblog_settings.html'
    model = WeblogSettings

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['data'] = WeblogSettings.objects.first()
        return context
