from django import forms
from django.contrib.auth.forms import PasswordChangeForm
from django.forms import PasswordInput

from fluidsurf.apps.users.models import CustomUser


class ContactForm(forms.Form):
    from_email = forms.EmailField(required=True, widget=forms.TextInput(attrs={'placeholder': 'email@ejemplo.com'}))
    message = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Escribe aquí tu duda o comentario'}),
                              required=True)


class ChangeUserForm(forms.ModelForm):
    email = forms.EmailField()
    first_name = forms.CharField(max_length=25)
    last_name = forms.CharField(max_length=50)
    telefono = forms.CharField(max_length=15)
    pais = forms.CharField(max_length=50)
    zona = forms.CharField(max_length=50)

    first_name.widget = forms.TextInput(attrs={'placeholder': 'Escribe aquí tu nombre...'})
    last_name.widget = forms.TextInput(attrs={'placeholder': 'Escribe aquí tus apellidos...'})
    email.widget = forms.TextInput(attrs={'placeholder': 'Escribe aquí tu email...'})
    telefono.widget = forms.TextInput(attrs={'placeholder': 'Escribe aquí tu telefono...'})
    pais.widget = forms.TextInput(attrs={'placeholder': 'Escribe aquí tu pais...'})
    zona.widget = forms.TextInput(attrs={'placeholder': 'Escribe aquí tu zona...'})

    class Meta:
        model = CustomUser
        fields = ('email', 'first_name', 'last_name', 'telefono', 'pais', 'zona')


class PasswordChangeCustomForm(PasswordChangeForm):
    error_css_class = 'has-error'
    error_messages = {'password_incorrect':
                          "La contraseña es incorrecta. Por favor intentalo de nuevo."}
    old_password = forms.CharField(required=True, label='Anterior Contraseña',
                                   widget=PasswordInput(attrs={
                                       'class': 'form-control mb-5'}),
                                   error_messages={
                                       'required': 'La contraseña no puede estar en blanco.'})

    new_password1 = forms.CharField(required=True, label='Nueva Contraseña',
                                    widget=PasswordInput(attrs={
                                        'class': 'form-control mb-5'}),
                                    error_messages={
                                        'required': 'La contraseña no puede estar en blanco.'})
    new_password2 = forms.CharField(required=True, label='Repite tu Nueva Contraseña',
                                    widget=PasswordInput(attrs={
                                        'class': 'form-control'}),
                                    error_messages={
                                        'required': 'La contraseña no puede estar en blanco.'})

class PhotographerForm(forms.ModelForm):
    alias = forms.CharField(max_length=25)
    CV = forms.Textarea()
    profile_pic = forms.ImageField()
    main_pic = forms.ImageField()

    class Meta:
        model = CustomUser
        fields = ('alias', 'CV', 'profile_pic', 'main_pic')