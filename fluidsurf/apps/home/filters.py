import django_filters
from django.forms import TextInput
from django.utils.translation import ugettext_lazy as _

from fluidsurf.apps.home.models import Producto, Compra, Denuncia, SolicitudStock
from fluidsurf.apps.users.models import CustomUser, Pais, Spot, Area, Continente

AREA_CHOICES = (
        ('Europe', _("Europe")),
        ('Africa', _("Africa")),
        ('Asia', _("Asia")),
        ('Oceania', _("Oceania")),
        ('North America', _("North America")),
        ('South America', _("South America"))
    )


class ProductoFilter(django_filters.FilterSet):
    nombre = django_filters.CharFilter(lookup_expr='icontains', widget=TextInput(attrs={'placeholder': _('Name')}))
    spot = django_filters.ChoiceFilter(choices=AREA_CHOICES)
    user__alias = django_filters.CharFilter(widget=TextInput(attrs={'placeholder': _('Photographer')}))
    user__username = django_filters.CharFilter(widget=TextInput(attrs={'placeholder': _('Photographer')}))
    fecha = django_filters.DateFilter()

    class Meta:
        model = Producto
        fields = ['nombre', 'user__alias', 'spot', 'user__username', 'fecha']


class PhotographerFilter(django_filters.FilterSet):
    zona = django_filters.ChoiceFilter(choices=AREA_CHOICES)
    alias = django_filters.CharFilter(lookup_expr='icontains', widget=TextInput(attrs={'placeholder': _('Username')}))

    class Meta:
        model = CustomUser
        fields = ['alias', 'zona']


#------------- Filtros de dashboard

class UserFilter(django_filters.FilterSet):
    username = django_filters.CharFilter(lookup_expr='icontains',
                                      widget=TextInput(attrs={'placeholder': _('Username')}))
    class Meta:
        model = CustomUser
        fields = ['username']


class CompraFilter(django_filters.FilterSet):
    comprador__username = django_filters.CharFilter(widget=TextInput(attrs={'placeholder': _('Comprador')}))
    vendedor__username = django_filters.CharFilter(widget=TextInput(attrs={'placeholder': _('Vendedor')}))
    fecha = django_filters.DateFilter()

    class Meta:
        model = Compra
        fields = ['comprador__username', 'vendedor__username', 'fecha']


class ZonaFilter(django_filters.FilterSet):
    nombre = django_filters.CharFilter(widget=TextInput(attrs={'placeholder': _('Spot')}))
    area__nombre = django_filters.CharFilter(widget=TextInput(attrs={'placeholder': _('Area')}))
    area__pais__nombre = django_filters.CharFilter(widget=TextInput(attrs={'placeholder': _('Pais')}))
    area__pais__continente__nombre = django_filters.CharFilter(widget=TextInput(attrs={'placeholder': _('Continente')}))

    class Meta:
        model = Spot
        fields = ['nombre', 'area__nombre', 'area__pais', 'area__pais__continente']


class PaisFilter(django_filters.FilterSet):
    nombre = django_filters.CharFilter(widget=TextInput(attrs={'placeholder': _('Pais')}))
    continente__nombre = django_filters.CharFilter(widget=TextInput(attrs={'placeholder': _('Continente')}))

    class Meta:
        model = Pais
        fields = ['nombre', 'continente']


class DenunciaFilter(django_filters.FilterSet):
    emisor__username = django_filters.CharFilter(lookup_expr='icontains', widget=TextInput(attrs={'placeholder': _('Emisor')}))
    receptor__username = django_filters.CharFilter(widget=TextInput(attrs={'placeholder': _('Receptor')}))

    class Meta:
        model = Denuncia
        fields = ['emisor__username', 'receptor__username']


class SolicitudFilter(django_filters.FilterSet):
    user__username = django_filters.CharFilter(lookup_expr='icontains', widget=TextInput(attrs={'placeholder': _('Usuario')}))
    product__nombre = django_filters.CharFilter(widget=TextInput(attrs={'placeholder': _('Producto')}))

    class Meta:
        model = SolicitudStock
        fields = ['user__username', 'product__nombre']


