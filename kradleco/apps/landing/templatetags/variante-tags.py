from django import template

from kradleco.apps.landing.models import VarianteArticulo

register = template.Library()


@register.simple_tag
def get_distinct_variantes_secundarias(articulo):
    list = []
    variantes = VarianteArticulo.objects.filter(articulo=articulo)
    for variante in variantes:
        if not (variante.opcion_2_value in list) and variante.opcion_2_value is not None:
            list.append(variante.opcion_2_value)
    return list if len(list) > 0 else False


@register.simple_tag
def get_variaciones_principales(articulo, variante_secundaria):
    variantes = VarianteArticulo.objects.filter(articulo=articulo, opcion_2_value=variante_secundaria)

    return variantes if variantes is not None else False
