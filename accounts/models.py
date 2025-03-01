from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .manager import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, max_length=255)
    full_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=11, unique=True)
    username = models.CharField(max_length=50, unique=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    user_profile_image = models.ImageField(upload_to='static/images/profile', null=True, blank=True)
    bio = models.TextField(max_length=500, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['username', 'email', 'full_name']
    readonly_fields = ['is_active', 'is_admin', 'is_superuser']
    objects = UserManager()



    def __str__(self):
        return self.full_name

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin
