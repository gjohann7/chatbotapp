# -*- coding: utf-8 -*-
from django.contrib import admin
from django.urls import include, path, re_path
from django.views.generic import TemplateView

"""
The URL patterns for the project and its apps.
"""
urlpatterns = [
    path('profile/', include(('chatbotapp.accounts.urls', 'accounts'))),
    path('conversation/', include(('chatbotapp.chatbot.urls', 'chatbot'))),
    path('admin/', admin.site.urls),
    re_path(r'^([^\s])*service-worker', TemplateView.as_view(
        template_name="js/service-worker.js",
        content_type='text/javascript'
    ), name='service-worker.js'),
    path('', include(('chatbotapp.core.urls', 'core')))
]

"""
Definition of the 400 error view.
"""
handler400 = TemplateView.as_view(
    template_name='core/400.html', content_type='text/html')
"""
Definition of the 403 error view.
"""
handler403 = TemplateView.as_view(
    template_name='core/403.html', content_type='text/html')
"""
Definition of the 404 error view.
"""
handler404 = TemplateView.as_view(
    template_name='core/404.html', content_type='text/html')
"""
Definition of the 500 error view.
"""
handler500 = 'chatbotapp.core.views.error_500_view'
