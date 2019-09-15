from kradleco.apps.users.models import CustomUser
from .models import PropuestaComercial
from django.db.models import Q
import django_filters

class PropuestaFilter(django_filters.FilterSet):
    recibidos = django_filters.BooleanFilter(
        label='Recibidos',
        method='filter_recibidos',
        # widget=CustomCheckboxFilter()
    )

    enviados = django_filters.BooleanFilter(
        label='Enviados',
        method='filter_enviados',
        # widget=CustomCheckboxFilter()
    )

    class Meta:
        model = PropuestaComercial
        fields = ['recibidos']

    # FUNCIONES DE FILTRADO DE LA BÚSQUEDA
    def filter_recibidos(self, queryset, name, value):
        if value:
            print("si")
            return queryset.filter(estado=True)
        else:
            print("no")
            return queryset

    def filter_enviados(self, queryset, name, value):
        if value:
            print("si")
            return queryset.filter(estado=True)
        else:
            print("no")
            return queryset
