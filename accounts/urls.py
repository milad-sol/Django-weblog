from django.urls import path, include
from . import views

app_name = 'accounts'
mobile_urlpatterns = [
    path('login-mobile/', views.UserLoginMobileView.as_view(), name='login_mobile'),
    path('verify-otp/', views.VerifyOtpCodeMobileView.as_view(), name='verify_otp'),

]
urlpatterns = [
    path('register/', views.UserRegisterView.as_view(), name='register'),
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('profile/<str:username>/', views.UserProfileView.as_view(), name='profile'),
    path('logout/', views.UserLogoutView.as_view(), name='logout'),
    path('edit-profile/<str:username>/', views.UserEditProfileView.as_view(), name='edit_profile'),
    path('', include((mobile_urlpatterns, ''))),
]
