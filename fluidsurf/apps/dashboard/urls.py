from django.urls import path

from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('productos', views.productos, name='productos'),
    path('compras', views.compras, name='compras'),
    path('zonas', views.zonas, name='zonas'),
    path('usuarios', views.usuarios, name='usuarios'),
    path('denuncias', views.denuncias, name='denuncias'),
    path('validar', views.validar, name='validar'),
    path('solicitud', views.solicitud, name='solicitudes'),
    path('perfil/<id>', views.perfil, name='perfil_admin'),
    path('watermark', views.watermark, name='watermark'),

    # Dashboard de fotografo
    path('fotografo', views.fotografo, name='fotografo'),
]
