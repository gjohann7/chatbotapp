# -*- coding: utf-8 -*-
from django.urls import path, re_path
from django.views.generic import TemplateView
from django.contrib.auth.views import LogoutView
from .views import index, CustomLoginView

"""
The URL patterns to match the core app routes.
"""
urlpatterns = [
    path('logout/', LogoutView.as_view(next_page='core:index', ), name="logout"),
    path('login/', CustomLoginView.as_view(), name="login"),
    path('accessibility/', TemplateView.as_view(
        template_name="core/accessibility.html",
        content_type='text/html'),
        name="accessibility"),
    path('', index, name="index")
]
