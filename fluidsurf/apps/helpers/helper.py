from datetime import date, timedelta

from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.utils.translation import ugettext_lazy as _

from fluidsurf.apps.dashboard.models import RegistroCompras, RegistroFotografos, RegistroSurferos

AREA_CHOICES = (
    ('Europe', _("Europe")),
    ('Africa', _("Africa")),
    ('Asia', _("Asia")),
    ('Oceania', _("Oceania")),
    ('North America', _("North America")),
    ('South America', _("South America"))
)


def registros_vacios_compras(user=0):
    if user != 0:
        registro_last = RegistroCompras.objects.filter(user=user).last()
    else:
        registro_last = RegistroCompras.objects.filter().last()
    if registro_last:
        diferencia = (date.today() - registro_last.fecha).days

        for dia in reversed(range(0, diferencia)):
            fecha = date.today() - timedelta(days=dia)
            if user != 0:
                registro = RegistroCompras.objects.filter(fecha=fecha, user=user).first()
            else:
                registro = RegistroCompras.objects.filter(fecha=fecha).first()
            if not registro:
                registro = RegistroCompras()
                registro.compras = 0
                registro.fecha = fecha
                if user != 0:
                    registro.user = user
            else:
                registro.compras += 1

            registro.save()


def registros_vacios_fotografos():
    registro_photo_last = RegistroFotografos.objects.last()

    if registro_photo_last:
        diferencia = (date.today() - registro_photo_last.fecha).days

        for dia in reversed(range(0, diferencia)):
            fecha = date.today() - timedelta(days=dia)
            registro_exists = RegistroFotografos.objects.filter(fecha=fecha).first()
            if not registro_exists:
                registro = RegistroFotografos()
                registro.users = 0
                registro.fecha = fecha
                registro.save()


def registros_vacios_surferos():
    registro_surf_last = RegistroSurferos.objects.last()
    
    if registro_surf_last:
        diferencia = (date.today() - registro_surf_last.fecha).days

        for dia in reversed(range(0, diferencia)):
            fecha = date.today() - timedelta(days=dia)
            registro_exists = RegistroSurferos.objects.filter(fecha=fecha).first()
            if not registro_exists:
                registro = RegistroSurferos()
                registro.users = 0
                registro.fecha = fecha
                registro.save()


# Desplegable de antigüedad en users.Empresa y users.Autonomo
ANTG1 = '1año'
ANTG2 = '1a2años'
ANTG3 = '2a5años'
ANTG4 = '5años'

ANTIGUEDAD = [
    ('', 'Antigüedad'),
    (ANTG1, 'menos de 1 año'),
    (ANTG2, '1-2 años'),
    (ANTG3, '2-5 años'),
    (ANTG4, 'más de 5 años'),
]


# Desplegable de facturación en users.Empresa y users.Autonomo
FACT1 = 'NoFacturado'
FACT2 = '0-5000'
FACT3 = '5000-20000'
FACT4 = '20000-100000'
FACT5 = '100000'

FACTURACION = [
    ('', 'Rango de facturación mensual'),
    (FACT1, 'Aún no he facturado'),
    (FACT2, '0€ - 5.000€'),
    (FACT3, '5.000€ - 20.000€'),
    (FACT4, '20.000€ - 100.000€'),
    (FACT5, 'más de 100.000€'),
]


def news_to_get(how_much_news):
    items = 0

    if how_much_news > 0:
        items = how_much_news // 3

    if items > 3:
        items = 9
    else:
        items = items * 3

    return items


def users_to_get(how_much_users):
    items = 0

    if how_much_users > 0:
        items = how_much_users // 2

    if items > 4:
        items = 8
    else:
        items = items * 2

    return items


def grouped(l, n):
    for i in range(0, len(l), n):
        yield l[i:i+n]


def enviar_email(subject, message):
    try:
        send_mail(subject, message, 'contact@fluidsurf.es', [
            'info@fluidsurf.es', 'rafa@quitiweb.com'])
    except BadHeaderError:
        return HttpResponse('Invalid header found')


class Tabs:
    def __init__(self, tab1_marked, tab1_hide, tab2_marked, tab2_hide):
        self.tab1_marked = tab1_marked
        self.tab1_hide = tab1_hide
        self.tab2_marked = tab2_marked
        self.tab2_hide = tab2_hide


def tab_selected(tab_number):
    if tab_number == 1:
        return Tabs('marked', '', '', 'hide')
    else:
        return Tabs('', 'hide', 'marked', '')
