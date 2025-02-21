from django.urls import path
from . import views

app_name = 'weblog_settings'

urlpatterns = [
    path("", views.WeblogSettingsView.as_view(), name='weblog_settings'),
]
