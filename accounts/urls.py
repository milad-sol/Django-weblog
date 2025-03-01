from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('register/', views.UserRegisterView.as_view(), name='register'),
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('profile/<str:username>/', views.UserProfileView.as_view(), name='profile'),
    path('logout/', views.UserLogoutView.as_view(), name='logout'),
    path('edit-profile/<str:username>/', views.UserEditProfileView.as_view(), name='edit_profile'),
]
