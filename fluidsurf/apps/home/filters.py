import django_filters
from django.forms import TextInput
from django.utils.translation import ugettext_lazy as _

from fluidsurf.apps.home.models import Producto
from fluidsurf.apps.users.models import CustomUser


class ProductoFilter(django_filters.FilterSet):
    nombre = django_filters.CharFilter(lookup_expr='icontains', widget=TextInput(attrs={'placeholder': _('Name')}))
    spot = django_filters.CharFilter(lookup_expr='icontains', widget=TextInput(attrs={'placeholder': _('Spot')}))
    user__alias = django_filters.CharFilter(widget=TextInput(attrs={'placeholder': _('Photographer')}))

    class Meta:
        model = Producto
        fields = ['nombre', 'user__alias', 'spot']

AREA_CHOICES = (
        ('Europe', _("Europe")),
        ('Africa', _("Africa")),
        ('Asia', _("Asia")),
        ('Oceania', _("Oceania")),
        ('North America', _("North America")),
        ('South America', _("South America"))
    )


class PhotographerFilter(django_filters.FilterSet):
    zona = django_filters.ChoiceFilter(choices=AREA_CHOICES)
    alias = django_filters.CharFilter(lookup_expr='icontains', widget=TextInput(attrs={'placeholder': _('Username')}))

    class Meta:
        model = CustomUser
        fields = ['alias', 'zona']
