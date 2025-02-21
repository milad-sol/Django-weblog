from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .forms import UserChangeForm, UserCreationForm
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    readonly_fields = ['last_login', ]
    list_display = ('email', 'full_name', 'is_admin', 'is_superuser')
    list_filter = ('is_admin', 'is_superuser')
    fieldsets = [
        ('Main', {'fields': ['email', 'password']}),
        ('Personal info', {'fields': ['full_name', 'phone_number']}),
        ('Permissions',
         {'fields': ['is_active', 'is_admin', 'is_superuser', 'last_login', 'groups', 'user_permissions']}),
    ]
    search_fields = ['email', 'full_name', 'phone_number']
    ordering = ('email',)
    filter_horizontal = ('groups', 'user_permissions')
    add_fieldsets = [
        ('Main', {'fields': ['full_name', 'phone_number', 'email', 'password', 'password2']}),
    ]
