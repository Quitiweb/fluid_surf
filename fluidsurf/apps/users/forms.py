from django import forms

# from localflavor.es.forms import ESIdentityCardNumberField

from django.contrib.auth.forms import UserCreationForm

from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = CustomUser
        fields = ('tipo_de_usuario', 'username', 'email')
