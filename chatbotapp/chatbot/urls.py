# -*- coding: utf-8 -*-
from django.urls import path, re_path
from .views import conversation, handle_message

"""
The URL patterns to match the chatbot app routes.
"""
urlpatterns = [
    path('', conversation, name="conversation"),
    path('question=<message>', handle_message)
]
