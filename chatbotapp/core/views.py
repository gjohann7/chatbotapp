# -*- coding: utf-8 -*-
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from .models import Contact
from .forms import ContactForm

template = 'core/'


class CustomAuthenticationForm(AuthenticationForm):
    """Definition of a Django-authentication-form-based form.

    Inherits from AuthenticationForm (class), a base class for
    authenticating users.

    Attributes
    ----------
    error_messages : dict
        Error message key-value pair.
    """
    error_messages = {
        'invalid_login': "Dados inválidos. Tente novamente."
    }


class CustomLoginView(LoginView):
    """Definition of a Django-login-view-based class.

    Inherits from LoginView (class), display the login form and
    handle the login action.

    Attributes
    ----------
    template_name : str
        The login view file path.
    authentication_form : class
        Django-authentication-form-based form.
    """
    template_name = 'accounts/login.html'
    authentication_form = CustomAuthenticationForm


def index(request):
    """Definition of the app index view.

    Parameters
    ----------
    request : HttpRequest
        The client request to the server.

    Returns
    -------
    HttpResponse
        The server response to the client.
    """
    form = ContactForm(request.POST or None)
    context = {}
    if form.is_valid():
        form.save()
        request.session['success'] = True
        request.session['was_reloaded'] = False
        return redirect('/#contact')
    else:
        if 'was_reloaded' in request.session:
            if not request.session['was_reloaded']:
                request.session['was_reloaded'] = True
            else:
                request.session['success'] = False
    context['form'] = form
    return render(request, template + 'index.html', context)


def error_500_view(request):
    """Definition of the 500 error view.

    Parameters
    ----------
    request : HttpRequest
        The client request to the server.

    Returns
    -------
    HttpResponse
        The server response to the client.
    """
    return render(request, 'core/500.html')
