from django.urls import path
from . import views

app_name = 'posts'

urlpatterns = [
    path('<slug:slug>/create-new-post/', views.CreatePostView.as_view(), name='post-create'),
    path('<slug:slug>/', views.PostDetailView.as_view(), name='post-detail'),
    path('delete/<slug:slug>/', views.PostDeleteView.as_view(), name='post-delete'),

]
