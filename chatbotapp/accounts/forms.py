# -*- coding: utf-8 -*-
import re
from django import forms
from django.contrib.auth import get_user_model
from django.core import validators
from .models import PasswordReset
from chatbotapp.core.utils import generate_hash_key, introductory_messages
from chatbotapp.core.mail import send_mail_template

User = get_user_model()


class RegisterForm(forms.ModelForm):
    """Definition of the user registration form.

    Inherits from forms.ModelForm (class), the main implementation of
    all the Model Form logic.

    Raises
    ------
    forms.ValidationError
        A password mismatch exception occurs when both password
        fields don't match.
    """
    username = forms.CharField(
        label='Usuário', min_length=4, max_length=15)
    email = forms.EmailField(label='E-mail', max_length=60)
    password1 = forms.CharField(
        label='Senha', widget=forms.PasswordInput,
        min_length=6,
        validators=[validators.RegexValidator(
            re.compile(r'^\S+$'),
            'Senha não pode conter espaço em branco', 'invalid_character'),
            validators.RegexValidator(
            re.compile(r'(?!^\d+$)^\S+$'),
            'Senha não pode conter só números', 'invalid_password')
        ],
        help_text='A senha não pode conter espaço em branco, ser inteiramente numérica e menos de 6 letras.')
    password2 = forms.CharField(
        label='Confirmação de senha', widget=forms.PasswordInput, min_length=6,)

    def clean_password2(self):
        """Validation of the password match.

        Returns
        -------
        str
            The user password entered in the form.

        Raises
        ------
        forms.ValidationError
            A password mismatch exception occurs when both password
            fields don't match.
        """
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('As duas senhas não são iguais.',
                                        code='password_mismatch')
        return password2

    def save(self):
        """
        Persists the user in the database.
        """
        user = super(RegisterForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        user.save()
        introductory_messages(user)
        return user

    class Meta:
        model = User
        fields = ['username', 'email']


class PasswordResetForm(forms.Form):
    """Definition of the user password reset form.

    Parameters
    ----------
    forms.Form : class
        A collection of Fields, plus their associated data.

    Raises
    ------
    forms.ValidationError
        An email not found exception occurs when the entered email
        doesn't exist in the database.
    """
    email = forms.EmailField(label="E-mail", max_length=60)

    def clean_email(self):
        """Validation of the email consistency.

        Returns
        -------
        str
            The user email entered in the form.

        Raises
        ------
        forms.ValidationError
            An email not found exception occurs when the entered email
            doesn't exist in the database.
        """
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            return email
        raise forms.ValidationError(
            'Este e-mail não está registrado')

    def save(self):
        """
        Persists the password reset request in the database.
        """
        user = User.objects.get(email=self.cleaned_data['email'])
        key = generate_hash_key(user.username)
        reset = PasswordReset(key=key, user=user)
        reset.save()
        context = {
            'user': user,
            'reset': reset
        }
        send_mail_template('Criar nova senha',
                           'accounts/password_reset_mail.html', context, [user.email])


class EditAccountForm(forms.ModelForm):
    """Definition of the user password reset form.

    Parameters
    ----------
    forms.ModelForm : class
        The main implementation of all the Model Form logic.

    Raises
    ------
    forms.ValidationError
        An email found exception occurs when the entered email
        already exists in the database.
    """
    username = forms.CharField(
        label='Usuário', min_length=4, max_length=15,
        validators=[validators.RegexValidator(re.compile(r'^[a-zA-Z0-9]+$'),
                                              'Permite-se apenas letras e números.', 'invalid')])

    def clean_email(self):
        """Validation of the email consistency.

        Returns
        -------
        str
            The user email entered in the form.

        Raises
        ------
        forms.ValidationError
            An email found exception occurs when the entered email
            already exists in the database.
        """
        email = self.cleaned_data['email']
        queryset = User.objects.filter(
            email=email).exclude(pk=self.instance.pk)
        if queryset.exists():
            raise forms.ValidationError(
                'Este e-mail pertence a outro usuário.')
        return email

    class Meta:
        model = User
        fields = ['username', 'email']
