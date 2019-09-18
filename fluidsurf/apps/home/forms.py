from django import forms

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
    direccion = forms.CharField(max_length=50)

    first_name.widget = forms.TextInput(attrs={'placeholder': 'Escribe aquí tu nombre...'})
    last_name.widget = forms.TextInput(attrs={'placeholder': 'Escribe aquí tus apellidos...'})
    email.widget = forms.TextInput(attrs={'placeholder': 'Escribe aquí tu email...'})
    telefono.widget = forms.TextInput(attrs={'placeholder': 'Escribe aquí tu telefono...'})
    direccion.widget = forms.TextInput(attrs={'placeholder': 'Escribe aquí tu direccion...'})

    class Meta:
        model = CustomUser
        fields = ('email', 'first_name', 'last_name', 'telefono', 'direccion')
