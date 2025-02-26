from django.urls import path
from . import views

app_name = 'posts'

urlpatterns = [
    path('create-new-post/', views.CreatePostView.as_view(), name='post-create'),
    path('<slug:slug>/', views.PostDetailView.as_view(), name='post-detail'),
    path('delete/<slug:slug>/', views.PostDeleteView.as_view(), name='post-delete'),
    path('edit/<slug:slug>/', views.PostUpdateView.as_view(), name='post-update'),


]
