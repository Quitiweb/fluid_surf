from django import forms
from django.contrib.auth.forms import PasswordChangeForm
from django.forms import PasswordInput
from django.utils.translation import ugettext_lazy as _


from fluidsurf.apps.home.models import Producto, Denuncia, Devolucion


class ContactForm(forms.Form):
    from_email = forms.EmailField(
        required=True, widget=forms.TextInput(attrs={'placeholder': 'email@domain.com'}))
    message = forms.CharField(
        widget=forms.Textarea(attrs={'placeholder': _('Write here your doubt or comment')}),
        required=True
    )


class PasswordChangeCustomForm(PasswordChangeForm):
    error_css_class = 'has-error'
    error_messages = {
        'password_incorrect': _("Wrong password. Please, try again."),
        'password_mismatch': _("Your passwords don't match"),
    }
    old_password = forms.CharField(
        required=False, label=_('Old Password'),
        widget=PasswordInput(attrs={'class': 'form-control mb-5'}),
        error_messages={'required': _('Your password cannot be empty')}
    )

    new_password1 = forms.CharField(
        required=False, label=_('New password'),
        widget=PasswordInput(attrs={'class': 'form-control mb-5'}),
        error_messages={'required': _('Your password cannot be empty')}
    )
    new_password2 = forms.CharField(
        required=False, label=_('Repeat your new password'),
        widget=PasswordInput(attrs={'class': 'form-control'}),
        error_messages={'required': _('Your password cannot be empty')}
    )


class AddProductForm(forms.ModelForm):

    DATE_INPUT_FORMATS = ['%d/%m/%Y']

    nombre = forms.CharField(required=True)
    precio = forms.CharField(required=True)

    fecha = forms.DateField(required=True, input_formats=DATE_INPUT_FORMATS)
    descripcion = forms.CharField(required=False)

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

    fecha.widget = forms.TextInput(
        attrs={'placeholder': _('Write when are you selling your product...')})
    nombre.widget = forms.TextInput(attrs={'placeholder': _("Write your product's name...")})
    precio.widget = forms.TextInput(attrs={'placeholder': '???'})
    descripcion.widget = forms.TextInput(
        attrs={'placeholder': _('Add a brief description about your product...')})

    class Meta:
        model = Producto
        fields = (
            'nombre', 'precio', 'fecha', 'descripcion', 'imagen0', 'imagen1', 'imagen2',
            'imagen3', 'imagen4', 'imagen5', 'imagen6', 'imagen7', 'imagen8', 'imagen9'
        )


class EditProductForm(forms.ModelForm):
    nombre = forms.CharField(required=True)
    precio = forms.CharField(required=True)
    descripcion = forms.CharField(required=False)

    class Meta:
        model = Producto
        fields = ('nombre', 'precio', 'descripcion')


class DenunciaForm(forms.ModelForm):
    CHOICES = (
        ('MAL USO', _("Bad usage of the app")),
        ('INAPROPIADO', _("Innapropiate content")),
        ('SPAM', _("Spam")),
        ('OTRO', _("Other")),
    )

    motivo = forms.ChoiceField(required=True, choices=CHOICES)
    detalles = forms.CharField(
        required=True,
        widget=forms.Textarea(attrs={
            'placeholder': _('Tell us more about the reason you are reporting this user.')}),
    )

    class Meta:
        model = Denuncia
        fields = ('motivo', 'detalles')


class DevolucionForm(forms.ModelForm):
    CHOICES = (
        ('Dead on Arrival', _("Dead on Arrival")),
        ('Faulty', _("Faulty, please supply details")),
        ('Order Error', _("Order Error")),
        ('Other', _("Other, please supply details")),
        ('Wrong Item', _("Received Wrong Item"))
    )

    BOOL_CHOICES = (
        (True, _("Yes")),
        (False, _("No"))
    )

    product = forms.ModelChoiceField(queryset=None)

    reason = forms.ChoiceField(choices=CHOICES, required=True)
    is_opened = forms.ChoiceField(choices=BOOL_CHOICES, required=True)

    details = forms.Textarea()

    def __init__(self, user, *args, **kwargs):
        super(DevolucionForm, self).__init__(*args, **kwargs)
        self.fields['product'].queryset = Producto.objects.all().filter(compra_p__comprador=user)
        self.fields["details"].required = False

    class Meta:
        model = Devolucion
        fields = ('product', 'reason', 'is_opened', 'details')
