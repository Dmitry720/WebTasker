from django import forms
from django.contrib.auth import password_validation
from django.contrib.auth.forms import UserCreationForm, UsernameField
from django.forms import ModelForm
from django.utils.translation import gettext_lazy as _

from tasker.models import User


class UserSettingForm(ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username']


class UserCreateForm(UserCreationForm):
    first_name = forms.CharField(required=True, label="First name", max_length=30)
    last_name = forms.CharField(required=True, label="Last name", max_length=30)
    email = forms.EmailField(required=True, label="Email address", max_length=30)
    username = UsernameField(required=True, label="Username", max_length=30)
    password1 = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput,
        help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        label=_("Password confirmation"),
        widget=forms.PasswordInput,
        strip=False,
        help_text=_("Enter the same password as before, for verification."),
    )

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'username', 'password1', 'password2')
