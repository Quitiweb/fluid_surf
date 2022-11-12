from django import forms
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


class ChangeUserForm(forms.ModelForm):
    email = forms.EmailField()
    first_name = forms.CharField(max_length=25)
    last_name = forms.CharField(max_length=50)
    telefono = forms.CharField(max_length=15)
    pais = forms.CharField(max_length=50)

    first_name.widget = forms.TextInput(attrs={'placeholder': _('Write your name here...')})
    last_name.widget = forms.TextInput(attrs={'placeholder': _('Write your surname here...')})
    email.widget = forms.TextInput(attrs={'placeholder': _('Write your email here...')})
    telefono.widget = forms.TextInput(attrs={'placeholder': _('Write your phone here...')})
    pais.widget = forms.TextInput(attrs={'placeholder': _('Write your country here...')})

    class Meta:
        model = CustomUser
        fields = ('email', 'first_name', 'last_name', 'telefono', 'pais')


class ChangeUserPostForm(forms.ModelForm):

    class Meta:
        model = CustomUser
        fields = ('email', 'first_name', 'last_name', 'telefono', 'pais')


class PhotographerForm(forms.ModelForm):
    alias = forms.CharField(max_length=25)
    CV = forms.Textarea()
    profile_pic = forms.ImageField()
    main_pic = forms.ImageField()

    class Meta:
        model = CustomUser
        fields = ('alias', 'CV', 'profile_pic', 'main_pic')
