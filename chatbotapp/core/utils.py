# -*- coding: utf-8 -*-
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _
import hashlib
import string
import random
from chatbotapp.chatbot.models import Message


class CustomNumericPasswordValidator:
    """
    Definition of a password validator, which validates if
    the password isn't composed only by numbers.
    """

    def validate(self, password, user=None):
        """Definition of the validation method.

        Parameters
        ----------
        password : str
            The password entered in a form.
        user : dict, optional
            The user data, by default None

        Raises
        ------
        ValidationError
            The password entirely numeric exceptions occurs when a password
            if composed only by numbers.
        """
        if password.isdigit():
            raise ValidationError(
                "Esta senha é inteiramente numérica.",
                code='password_entirely_numeric',
            )

    def get_help_text(self):
        """Definition of the help text in case of a fail validation.

        Returns
        -------
        str
            The help text.
        """
        return 'Senha não pode ser inteiramente numérica'


class CustomMinimumLengthValidator:
    """
    Definition of a password validator, which validates if
    the password isn't too short.

    Parameters
    ----------
    min_length : int, optional
        The minimum length of the password, by defaul 6.
    """

    def __init__(self, min_length=6):
        self.min_length = min_length

    def validate(self, password, user=None):
        """Definition of the validation method.

        Parameters
        ----------
        password : str
            The password entered in a form.
        user : dict, optional
            The user data, by default None

        Raises
        ------
        ValidationError
            The invalid password exceptions occurs when a password
            is too short.
        """
        if len(password) < self.min_length:
            raise ValidationError(
                _('Nova senha muito curta.'))

    def get_help_text(self):
        """Definition of the help text in case of a fail validation.

        Returns
        -------
        str
            The help text.
        """
        return _('Senha deve conter pelo menos %(min_length)d caracteres') % {'min_length': self.min_length}


def generate_hash_key(salt, random_str_size=6):
    """Generates a hash key.

    Parameters
    ----------
    salt : str
        A user personal information.
    random_str_size : int, optional
        The length of the random key, by default 6

    Returns
    -------
    str
        A hash object digested as a string.
    """
    chars = string.ascii_uppercase + string.digits
    random_str = "".join(random.choice(chars) for i in range(random_str_size))
    text = random_str + salt
    return hashlib.sha224(text.encode('utf-8')).hexdigest()


def introductory_messages(user):
    """Persists the chatbot introductory messages to a new user.

    Parameters
    ----------
    user : class
        The new user data.
    """
    intro_one = ("Eu sou um chatbot, ou seja, um robô de conversação. " +
                 "Aqui, farei o papel de um paciente e você deve fazer a " +
                 "entrevista inicial e investigar em busca de sintomas " +
                 "ou sinais de alguma psicopatologia. Mais tarde, deverá " +
                 "apresentar sua hipótese diagnóstica inicial no formulário")
    intro_two = ("Meu personagem é do sexo masculino, adulto e vem tendo alguns problemas " +
                 "no dia a dia. Tome a iniciativa e bom estudo!")
    Message(content=intro_one, owner=user, is_bot=True).save()
    Message(content=intro_two, owner=user, is_bot=True).save()
