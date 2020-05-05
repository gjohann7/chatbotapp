# -*- coding: utf-8 -*-
from django.contrib import admin
from .models import Contact


class ContactAdmin(admin.ModelAdmin):
    """Definition of the contact management in the Admin page.

    Inherits from ModelAdmin (class), encapsulates all admin options
    and functionality for a given model.
    """
    list_display = ['name', 'email', 'created_at']
    search_fields = ['name', 'email', 'message', 'created_at']
    empty_value_display = '-vazio-'

    class Meta:
        model = Contact


admin.site.register(Contact, ContactAdmin)
