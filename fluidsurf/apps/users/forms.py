from django import forms

# TODO Por alguna razón, ESIdentityCardNumberField falla al importarlo
# from localflavor.es.forms import ESIdentityCardNumberField

from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import CustomUser, Empresa, GaleriaUsuario, Autonomo, MiPerfil
from ..helpers.helper import ANTIGUEDAD, FACTURACION


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = CustomUser
        fields = ('tipo_de_usuario', 'username', 'email')


class PublicUserForm(UserChangeForm):
    telefono = forms.CharField(required=False)

    class Meta:
        model = CustomUser
        fields = ('username', 'titular', 'sobre_mi_negocio', 'logo', 'foto_perfil', 'telefono', 'email', 'facebook',
                  'twitter', 'youtube', 'linkedin')

    def __init__(self, *args, **kwargs):
        super(PublicUserForm, self).__init__(*args, **kwargs)
        self.fields['sobre_mi_negocio'].widget.attrs['placeholder'] = 'Sobre mi negocio'
        self.fields['titular'].widget.attrs['placeholder'] = 'Titular'
        self.fields['telefono'].widget.attrs['placeholder'] = 'telefono'
        self.fields['email'].widget.attrs['placeholder'] = 'e-mail'
        self.fields['facebook'].widget.attrs['placeholder'] = 'Facebook'
        self.fields['youtube'].widget.attrs['placeholder'] = 'Youtube'
        self.fields['linkedin'].widget.attrs['placeholder'] = 'Linkedin'
        self.fields['twitter'].widget.attrs['placeholder'] = 'Twitter'


class MiPerfilSimpleUserForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'titular', 'sobre_mi_negocio', 'logo', 'foto_perfil', 'facebook',
                  'twitter', 'youtube', 'linkedin')

    def __init__(self, *args, **kwargs):
        super(MiPerfilSimpleUserForm, self).__init__(*args, **kwargs)
        self.fields['sobre_mi_negocio'].widget.attrs['placeholder'] = 'Sobre mi negocio'
        self.fields['titular'].widget.attrs['placeholder'] = 'Titular'
        self.fields['facebook'].widget.attrs['placeholder'] = 'Facebook'
        self.fields['youtube'].widget.attrs['placeholder'] = 'Youtube'
        self.fields['linkedin'].widget.attrs['placeholder'] = 'Linkedin'
        self.fields['twitter'].widget.attrs['placeholder'] = 'Twitter'


class NewImagenGaleriaForm(forms.ModelForm):
    class Meta:
        model = GaleriaUsuario
        fields = {'imagen'}


class CustomUserChangeForm(UserChangeForm):
    is_empresa = forms.BooleanField(
        required=False,
        initial=False,
        # widget=CustomCheckboxInput()
    )
    is_autonomo = forms.BooleanField(
        required=False,
        initial=False,
        # widget=CustomCheckboxInput()
    )

    is_empresa.widget.attrs.update({'class': 'toggle-chk'})
    is_autonomo.widget.attrs.update({'class': 'toggle-chk'})

    class Meta:
        model = CustomUser
        fields = ('email', 'first_name', 'last_name', 'telefono', 'is_empresa', 'is_autonomo')


class CustomUserMarcaEspacio(UserChangeForm):
    is_marca = forms.BooleanField(
        required=False,
        initial=False,
        # widget=CustomCheckboxInput()
    )

    is_espacio = forms.BooleanField(
        required=False,
        initial=False,
        # widget=CustomCheckboxInput()
    )

    is_marca.widget.attrs.update({'class': 'toggle-chk'})
    is_espacio.widget.attrs.update({'class': 'toggle-chk'})

    class Meta:
        model = CustomUser
        fields = ('is_marca', 'is_espacio')


class RazonSocialForm(forms.ModelForm):
    class Meta:
        model = Empresa
        fields = ('razon_social',)

    def __init__(self, *args, **kwargs):
        super(RazonSocialForm, self).__init__(*args, **kwargs)
        self.fields['razon_social'].widget.attrs['placeholder'] = 'Nombre/Razón social'


class MiPerfilForm(forms.ModelForm):
    negociable = forms.BooleanField(
        required=False,
        initial=False,
        # widget=CustomCheckboxInput()
    )

    is_espacio = forms.BooleanField(
        required=False,
        initial=False,
        # widget=CustomCheckboxInput()
    )

    is_marca = forms.BooleanField(
        required=False,
        initial=False,
        # widget=CustomCheckboxInput()
    )

    negociable.widget.attrs.update({'class': 'toggle-chk'})
    is_espacio.widget.attrs.update({'class': 'toggle-chk'})
    is_marca.widget.attrs.update({'class': 'toggle-chk'})

    class Meta:
        model = MiPerfil
        exclude = ('user',)


class EmpresaForm(forms.ModelForm):
    antiguedad = forms.ChoiceField(choices=ANTIGUEDAD, required=False)
    facturacion = forms.ChoiceField(choices=FACTURACION, required=False)

    # nif = ESIdentityCardNumberField()
    # nif.widget.attrs.update({'placeholder': 'NIF', 'required': 'false'})

    class Meta:
        model = Empresa
        fields = ('razon_social', 'antiguedad', 'facturacion', 'nif', 'iva',)

    def __init__(self, *args, **kwargs):
        super(EmpresaForm, self).__init__(*args, **kwargs)
        self.fields['razon_social'].widget.attrs['placeholder'] = 'Nombre/Razón social'
        self.fields['iva'].widget.attrs['placeholder'] = 'IVA'
        self.fields['nif'].widget.attrs['placeholder'] = 'NIF'


FIELD_NAME_MAPPING = {
    'razon_social': 'au_razon_social',
    'nif': 'au_nif',
    'antiguedad': 'au_antiguedad',
    'facturacion': 'au_facturacion',
    'iva': 'au_iva',
}


class AutonomoForm(forms.ModelForm):
    antiguedad = forms.ChoiceField(choices=ANTIGUEDAD, required=False)
    facturacion = forms.ChoiceField(choices=FACTURACION, required=False)
    # nif = ESIdentityCardNumberField()
    # nif.widget.attrs.update({'placeholder': 'NIF', 'required': 'false'})
    irpf = forms.CharField(required=False)

    class Meta:
        model = Autonomo
        fields = ('razon_social', 'nif', 'antiguedad', 'facturacion', 'iva', 'irpf',)

    def __init__(self, *args, **kwargs):
        super(AutonomoForm, self).__init__(*args, **kwargs)
        self.fields['razon_social'].widget.attrs['placeholder'] = 'Nombre/Razón social'
        self.fields['iva'].widget.attrs['placeholder'] = 'IVA'
        self.fields['irpf'].widget.attrs['placeholder'] = 'IRPF'
        self.fields['nif'].widget.attrs['placeholder'] = 'NIF'

    def add_prefix(self, field_name):
        # look up field name; return original if not found
        field_name = FIELD_NAME_MAPPING.get(field_name, field_name)
        return super(AutonomoForm, self).add_prefix(field_name)
