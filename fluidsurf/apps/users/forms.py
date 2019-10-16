from django import forms

# from localflavor.es.forms import ESIdentityCardNumberField

from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import ugettext_lazy as _

from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):

    CHOICES = (
        ('SURFERO', _('Surfer')),
        ('FOTOGRAFO', _('Photographer')),
    )

    tipo_de_usuario = forms.ChoiceField(choices=CHOICES)

    class Meta(UserCreationForm):
        model = CustomUser
        fields = ('tipo_de_usuario', 'username', 'email')
