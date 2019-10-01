from django import forms
from django.contrib.auth.forms import PasswordChangeForm
from django.forms import PasswordInput

from fluidsurf.apps.home.models import Producto
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
                          "La contraseña es incorrecta. Por favor intentalo de nuevo.",
                      'password_mismatch':
                          "Las contraseñas no coinciden",
                      }
    old_password = forms.CharField(required=False, label='Anterior Contraseña',
                                   widget=PasswordInput(attrs={
                                       'class': 'form-control mb-5'}),
                                   error_messages={
                                       'required': 'La contraseña no puede estar en blanco.'})

    new_password1 = forms.CharField(required=False, label='Nueva Contraseña',
                                    widget=PasswordInput(attrs={
                                        'class': 'form-control mb-5'}),
                                    error_messages={
                                        'required': 'La contraseña no puede estar en blanco.'})
    new_password2 = forms.CharField(required=False, label='Repite tu Nueva Contraseña',
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


class AddProductForm(forms.ModelForm):
    nombre = forms.CharField(required=True)
    precio = forms.CharField(required=True)

    fecha = forms.DateField(required=True)
    spot = forms.CharField(required=True)
    imagen0 = forms.ImageField(required=False)
    imagen1 = forms.ImageField(required=False)
    imagen2 = forms.ImageField(required=False)
    imagen3 = forms.ImageField(required=False)
    imagen4 = forms.ImageField(required=False)
    imagen5 = forms.ImageField(required=False)
    imagen6 = forms.ImageField(required=False)
    imagen7 = forms.ImageField(required=False)
    imagen8 = forms.ImageField(required=False)
    imagen9 = forms.ImageField(required=False)

    imagen1.widget.attrs['class'] = 'hide'
    imagen2.widget.attrs['class'] = 'hide'
    imagen3.widget.attrs['class'] = 'hide'
    imagen4.widget.attrs['class'] = 'hide'
    imagen5.widget.attrs['class'] = 'hide'
    imagen6.widget.attrs['class'] = 'hide'
    imagen7.widget.attrs['class'] = 'hide'
    imagen8.widget.attrs['class'] = 'hide'
    imagen9.widget.attrs['class'] = 'hide'

    imagen0.widget.attrs['class'] = 'imagenes'
    imagen1.widget.attrs['class'] = 'imagenes'
    imagen2.widget.attrs['class'] = 'imagenes'
    imagen3.widget.attrs['class'] = 'imagenes'
    imagen4.widget.attrs['class'] = 'imagenes'
    imagen5.widget.attrs['class'] = 'imagenes'
    imagen6.widget.attrs['class'] = 'imagenes'
    imagen7.widget.attrs['class'] = 'imagenes'
    imagen8.widget.attrs['class'] = 'imagenes'
    imagen9.widget.attrs['class'] = 'imagenes'

    imagen0.widget = forms.ClearableFileInput(attrs={'multiple': True})
    imagen1.widget = forms.ClearableFileInput(attrs={'multiple': True})
    imagen2.widget = forms.ClearableFileInput(attrs={'multiple': True})
    imagen3.widget = forms.ClearableFileInput(attrs={'multiple': True})
    imagen4.widget = forms.ClearableFileInput(attrs={'multiple': True})
    imagen5.widget = forms.ClearableFileInput(attrs={'multiple': True})
    imagen6.widget = forms.ClearableFileInput(attrs={'multiple': True})
    imagen7.widget = forms.ClearableFileInput(attrs={'multiple': True})
    imagen8.widget = forms.ClearableFileInput(attrs={'multiple': True})
    imagen9.widget = forms.ClearableFileInput(attrs={'multiple': True})

    fecha.widget = forms.TextInput(attrs={'placeholder': 'Introduce la fecha para vender tu producto...'})
    spot.widget = forms.TextInput(attrs={'placeholder': 'Escribe donde vas a estar...'})
    nombre.widget = forms.TextInput(attrs={'placeholder': 'Introduce el nombre de tu producto...'})
    precio.widget = forms.TextInput(attrs={'placeholder': '€'})

    class Meta:
        model = Producto
        fields = ('nombre', 'precio', 'fecha', 'spot', 'imagen0', 'imagen1', 'imagen2', 'imagen3', 'imagen4', 'imagen5'
                  , 'imagen6', 'imagen7', 'imagen8', 'imagen9')



