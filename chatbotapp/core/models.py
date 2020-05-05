# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models


class Contact(models.Model):
    """Definition of the contact model.

    Inherits from Model (class), a base definition of a model class.
    """
    name = models.CharField('Nome', max_length=50)
    email = models.EmailField('E-mail', max_length=50)
    message = models.TextField('Mensagem')
    created_at = models.DateTimeField(
        'Data de registro', auto_now=False, auto_now_add=True)

    def __unicode__(self):
        return 'Contact: ' + self.name + ' ' + str(self.email)

    def __str__(self):
        return 'Contact: ' + self.name + ' ' + str(self.email)

    class Meta:
        verbose_name = "Contato"
        verbose_name_plural = "Contatos"
        ordering = ['-created_at']
