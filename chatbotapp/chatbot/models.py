# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.conf import settings


class Message(models.Model):
    """Definition of the message model.

    Inherits models.Model (class), a base definition of a model class.
    """
    content = models.CharField(
        'Conteúdo da mensagem', max_length=700, blank=False, null=True)
    send_date = models.DateTimeField(
        'Data de envio', auto_now_add=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name="Usuário",
                              default=None, on_delete=models.CASCADE)
    is_bot = models.BooleanField(
        'É robô', blank=False, null=False, default=False)

    class Meta:
        verbose_name = "Mensagem"
        verbose_name_plural = "Mensagens"
        ordering = ['owner']

    def __unicode__(self):
        return self.owner.username

    def __str__(self):
        return self.owner.username
