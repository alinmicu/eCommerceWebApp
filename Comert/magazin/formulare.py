from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from crispy_forms.helper import FormHelper

class FormularInregistrare(UserCreationForm):
    email = forms.EmailField(max_length=250, required=True)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2')


class FormularContact(forms.Form):
    subiect = forms.CharField(max_length = 50, required = True)
    nume = forms.CharField(max_length = 50, required = True)
    email_expeditor = forms.EmailField(max_length = 50, required = True)
    mesaj = forms.CharField(max_length = 600, widget = forms.Textarea(), help_text='Scrieti aici mesajul!')
