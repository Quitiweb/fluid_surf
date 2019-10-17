import django_filters
from django.forms import TextInput
from django.utils.translation import ugettext_lazy as _

from fluidsurf.apps.home.models import Producto


class ProductoFilter(django_filters.FilterSet):
    nombre = django_filters.CharFilter(lookup_expr='icontains', widget=TextInput(attrs={'placeholder': _('Name')}))
    spot = django_filters.CharFilter(lookup_expr='icontains', widget=TextInput(attrs={'placeholder': _('Spot')}))
    user__username = django_filters.CharFilter(widget=TextInput(attrs={'placeholder': _('Photographer')}))

    class Meta:
        model = Producto
        fields = ['nombre', 'user__username', 'spot']
