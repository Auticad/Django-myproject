"""Admin utenti — apps/users/admin.py"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display  = ['email', 'username', 'is_verified', 'is_staff', 'date_joined']
    list_filter   = ['is_staff', 'is_verified', 'is_active']
    search_fields = ['email', 'username', 'first_name', 'last_name']
    ordering      = ['-date_joined']

    fieldsets = UserAdmin.fieldsets + (
        ('Profilo', {'fields': ('bio', 'avatar', 'is_verified', 'subscribe_newsletter')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Info extra', {'fields': ('email',)}),
    )
