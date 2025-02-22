from django.urls import path
from . import views

app_name = 'posts'

urlpatterns = [
    path('<slug:slug>/', views.PostDetailView.as_view(), name='post-detail'),
]
