from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('mi-cuenta', views.mi_cuenta, name='mi-cuenta'),
    path('change-image', views.change_image, name='change-image'),
    path('subir-producto', views.subir_producto, name='subir-producto'),
    path('producto/<id>', views.producto, name='producto'),
    path('zona/<nombre>', views.zona, name='zona'),
    path('perfil/<nombre>', views.perfil, name='perfil'),
    path('mensaje-enviado', views.mensaje_enviado, name='mensaje-enviado'),
    path('formulario', views.formulario, name='formulario'),
    path('solicitud-recibida', views.solicitud_recibida, name='solicitud-recibida'),
    path('wishlist', views.wishlist, name='wishlist'),
    path('historial', views.historial, name='historial'),
]
