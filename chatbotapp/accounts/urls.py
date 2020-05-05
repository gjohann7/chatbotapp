# -*- coding: utf-8 -*-
from django.contrib import admin
from django.urls import include, path
from .views import (
    register, password_reset, password_reset_confirmation,
    editable_profile, change_password
)

"""
The URL patterns to match the accounts app routes.
"""
urlpatterns = [
    path('register/', register, name='register'),
    path('password-reset/', password_reset, name='password_reset'),
    path('password-reset/confirmation/<key>/', password_reset_confirmation,
         name='password_reset_confirmation'),
    path('change-password/', change_password,
         name="change_password"),
    path('', editable_profile, name="editable_profile")
]
