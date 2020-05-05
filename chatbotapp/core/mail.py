# -*- coding: utf-8 -*-
from django.core.mail.backends.smtp import EmailBackend
from django.template.loader import render_to_string
from django.template.defaultfilters import striptags
from django.core.mail import EmailMultiAlternatives
from django.conf import settings


def send_mail_template(subject, template_name, context, recipient_list,
                       from_email=settings.DEFAULT_FROM_EMAIL, fail_silently=False):
    """Send mail definition.

    Parameters
    ----------
    subject : str
        The email subject.
    template_name : str
        The email template path.
    context : dict
        The context of the email message, which holds the email information.
    recipient_list : list
        An email list to send the emails.
    from_email : str, optional
        The sender email, by default settings.DEFAULT_FROM_EMAIL
    fail_silently : bool, optional
        Defines whether an error occurred when sending the email is raised,
        by default False
    """
    message_html = render_to_string(template_name, context)
    message_txt = striptags(message_html)
    email = EmailMultiAlternatives(
        subject=subject, body=message_txt, from_email=from_email,
        to=recipient_list
    )
    email.attach_alternative(message_html, 'text/html')
    email.send(fail_silently=fail_silently)
