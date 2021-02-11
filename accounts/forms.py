from django import forms
from django.forms import PasswordInput
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit


class CreateUserForm(forms.Form):
    """it's the form to signup """
    name = forms.CharField(label='Nom', max_length=100)
    surname = forms.CharField(label='Prénom', max_length=100)
    email = forms.EmailField(label='Adresse électronique ', max_length=100)
    password1 = forms.CharField(label='Mot de passe', widget=PasswordInput())
    password2 = forms.CharField(label='Ressaisir le mot de passe',
                                widget=PasswordInput())
    helper = FormHelper()
    helper.add_input(Submit('submit', 'Créer un compte', css_id="register-btn",
                            css_class='btn btn-primary btn-block'))
    helper.form_method = 'POST'
    helper.form_show_errors = True


class AuthenticateForm(forms.Form):
    """it's the form to login """
    username = forms.EmailField(label='Adresse électronique ', max_length=100)
    password = forms.CharField(label='Mot de passe', widget=PasswordInput())
    helper = FormHelper()
    helper.add_input(Submit('submit', 'Se connecter', css_id="login-btn",
                            css_class='btn btn-primary btn-block'))
    helper.form_method = 'POST'
    helper.form_show_errors = True
