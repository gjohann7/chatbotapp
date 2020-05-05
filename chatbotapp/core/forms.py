from django import forms
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from .models import Contact
from .mail import send_mail_template

template = 'core/'


class ContactForm(forms.Form):
    """Definition of the contact form.

    Inherits from Form (class), a collection of Fields, plus their associated data.

    Raises
    ------
    forms.ValidationError
        A minimum word exception occurs when the user entered less than
        two words in the message field of the contact form.
    """
    name = forms.CharField(label="Nome", min_length=3, max_length=50)
    email = forms.EmailField(label="E-mail", max_length=60)
    attrs = {'cols': '40', 'rows': '5'}
    message = forms.CharField(
        label="Mensagem", widget=forms.Textarea(attrs), min_length=5
    )

    def clean_message(self):
        """Validation of the message length.

        Returns
        -------
        str
            The user entered message.

        Raises
        ------
        forms.ValidationError
            A minimum word exception occurs when the user entered less than
            two words in the message field of the contact form.
        """
        message = self.cleaned_data['message']
        if len(message.split()) < 2:
            raise forms.ValidationError(
                # The message cannot be too short
                # A mensagem não pode ser muito curta
                message=_('A mensagem não pode ser muito curta'), code='min_words')
        return message

    def save(self):
        """
        Persists the contact message in the database, send emails to the site contact
        email about the new message and to the user who sent the message.
        """
        contact = Contact(
            name=self.cleaned_data['name'], email=self.cleaned_data['email'],
            message=self.cleaned_data['message'])
        contact.save()
        context = {
            'contact': contact
        }
        send_mail_template('Chatbot-App Contact',
                           template + 'contact.html', context, [settings.DEFAULT_FROM_EMAIL])
        send_mail_template('Chatbot-App Contact Reply',
                           template + 'contact_reply.html', context, [contact.email])
