# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import SetPasswordForm, PasswordChangeForm
from django.contrib.auth import authenticate, login, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.password_validation import MinimumLengthValidator
from django.core.exceptions import ValidationError
from .models import User, PasswordReset
from .forms import RegisterForm, PasswordResetForm, EditAccountForm
from django.core.exceptions import ValidationError

template = 'accounts/'


def register(request):
    """Definition of the user registration view.

    Parameters
    ----------
    request : HttpRequest
        The client request to the server.

    Returns
    -------
    HttpResponse
        The server response to the client.
    """
    form = RegisterForm(request.POST or None)
    if form.is_valid():
        user = form.save()
        user = authenticate(
            username=user.username,
            password=form.cleaned_data['password1'])
        login(request, user)
        return redirect('chatbot:conversation')

    context = {
        'form': form
    }
    return render(request, template + 'register.html', context)


def password_reset(request):
    """Definition of the user password reset view.

    Parameters
    ----------
    request : HttpRequest
        The client request to the server.

    Returns
    -------
    HttpResponse
        The server response to the client.
    """
    context = {}
    form = PasswordResetForm(request.POST or None)
    if form.is_valid():
        form.save()
        context['success'] = True
    context['form'] = form
    return render(request, template + 'password_reset.html', context)


def password_reset_confirmation(request, key):
    """Definition of the user password reset confirmation view.

    Parameters
    ----------
    request : HttpRequest
        The client request to the server.

    Returns
    -------
    HttpResponse
        The server response to the client.
    """
    context = {}
    reset = get_object_or_404(PasswordReset, key=key)
    form = SetPasswordForm(user=reset.user, data=request.POST or None)
    if form.is_valid():
        form.save()
        reset.confirmed = True
        reset.save()
        context['success'] = True
    context['form'] = form
    return render(request, template + 'password_reset_confirmation.html', context)


@login_required
def editable_profile(request):
    """Definition of the user profile view.

    This view also allows the user to edit its profile.

    Parameters
    ----------
    request : HttpRequest
        The client request to the server.

    Returns
    -------
    HttpResponse
        The server response to the client.
    """
    context = {}
    if request.method == 'POST':
        form = EditAccountForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            form = EditAccountForm(instance=request.user)
            context['success'] = True
    else:
        form = EditAccountForm(instance=request.user)
    context['form'] = form
    return render(request, template + 'editable_profile.html', context)


@login_required
def change_password(request):
    """Definition of the user password change view.

    Parameters
    ----------
    request : HttpRequest
        The client request to the server.

    Returns
    -------
    HttpResponse
        The server response to the client.
    """
    context = {}
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user)
        if form.is_valid():
            form.save()
            context['success'] = True
    else:
        form = PasswordChangeForm(user=request.user)

    if form.errors:
        if form.data:
            if form.error_messages['password_incorrect'] != '':
                form.error_messages['password_incorrect'] = 'Sua senha antiga está incorreta.'
            if form.error_messages['password_mismatch'] != '':
                form.error_messages['password_mismatch'] = 'As duas senhas não são iguais.'
        else:
            form = PasswordChangeForm(user=request.user)

    context['form'] = form
    return render(request, template + 'change_password.html', context)
