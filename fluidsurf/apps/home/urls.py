from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('/', views.index, name='index'),
    path('mensaje-enviado', views.mensaje_enviado, name='mensaje-enviado'),
    path('formulario', views.formulario, name='formulario'),
    path('solicitud-recibida', views.solicitud_recibida, name='solicitud-recibida'),
]
