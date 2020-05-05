# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import re
from django.db import models
from django.core import validators
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager


class User(AbstractBaseUser, PermissionsMixin):
    """Definition of the user model.

    Parameters
    ----------
    AbstractBaseUser : class
        The base of the user model.
    PermissionsMixin : class
        Add the fields and methods necessary to support the Group and Permission
        models using the ModelBackend.
    """
    username = models.CharField(
        'Usuário', max_length=15, unique=True,
        validators=[validators.RegexValidator(
            re.compile(r'^[a-zA-Z0-9]+$'), 'Permite-se apenas letras e números', 'invalid')],
        error_messages={'unique': 'Nome de usuário já existente'})
    email = models.EmailField('E-mail', max_length=60, unique=True)
    is_staff = models.BooleanField(
        'Membro da equipe', default=False)
    date_joined = models.DateTimeField(
        'Data de registro', auto_now=False, auto_now_add=True)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __unicode__(self):
        return self.username

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = "Usuário"
        verbose_name_plural = "Usuários"
        ordering = ['username']


class PasswordReset(models.Model):
    """Definition of the password reset model.

    Inherits models.Model (class), a base definition of a model class.
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             verbose_name='Usuário', related_name="reset", on_delete=models.CASCADE)
    key = models.CharField('Chave', max_length=100, unique=True)
    created_at = models.DateTimeField(
        "Criado em", auto_now=False, auto_now_add=True)
    confirmed = models.BooleanField('Confirmado', default=False)

    def __unicode__(self):
        return '{0} - {1}'.format(self.user, self.created_at)

    def __str__(self):
        return '{0} - {1}'.format(self.user, self.created_at)

    class Meta:
        verbose_name = 'Redefinição de senha'
        verbose_name_plural = 'Redefinições de senha'
        ordering = ['-created_at']
