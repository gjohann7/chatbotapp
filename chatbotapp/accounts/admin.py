# -*- coding: utf-8 -*-
from django.contrib import admin
from .models import User, PasswordReset


class UserAdmin(admin.ModelAdmin):
    """Definition of the user management in the Admin page.

    Inherits from ModelAdmin (class), encapsulates all admin options
    and functionality for a given model.
    """
    list_display = ['username', 'email',
                    'is_superuser', 'is_staff', 'date_joined', 'last_login']
    search_fields = ['username', 'email', 'date_joined', 'last_login']
    list_filter = ['is_superuser', 'is_staff']
    empty_value_display = '-vazio-'

    class Meta:
        model = User


admin.site.register(User, UserAdmin)


class PasswordResetAdmin(admin.ModelAdmin):
    """Definition of the password reset management in the Admin page.

    Parameters
    ----------
    admin : class
        Encapsulate all admin options and functionality for a given model.
    """
    list_display = ['user', 'key', 'created_at', 'confirmed']
    search_fields = ['user__username', 'key', 'created_at']
    list_filter = ['confirmed']
    empty_value_display = '-vazio-'

    class Meta:
        model = PasswordReset


admin.site.register(PasswordReset, PasswordResetAdmin)
