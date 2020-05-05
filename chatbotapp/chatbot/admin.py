# -*- coding: utf-8 -*-
from django.contrib import admin
from .models import Message


class MessageAdmin(admin.ModelAdmin):
    """Definition of the message management in the Admin page.

    Inherits from ModelAdmin (class), encapsulates all admin
    options and functionality for a given model.
    """
    list_display = ['owner', 'is_bot', 'content', 'send_date']
    search_fields = ['owner__username', 'content', 'send_date']
    list_filter = ['is_bot']
    empty_value_display = '-vazio-'

    class Meta:
        model = Message


admin.site.register(Message, MessageAdmin)
