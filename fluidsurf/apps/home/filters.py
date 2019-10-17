import django_filters

from fluidsurf.apps.home.models import Producto

class ProductoFilter(django_filters.FilterSet):
    nombre = django_filters.CharFilter(lookup_expr='icontains')
    class Meta:
        model = Producto
        fields = ['nombre']
