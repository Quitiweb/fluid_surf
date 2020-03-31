from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('mi-cuenta', views.mi_cuenta, name='mi-cuenta'),
    path('mis-productos', views.mis_productos, name='mis-productos'),
    path('change-image', views.change_image, name='change-image'),
    path('subir-producto', views.subir_producto, name='subir-producto'),
    path('producto/<id>', views.producto, name='producto'),
    path('zona/<nombre>', views.zona, name='zona'),
    path('perfil/<id>', views.perfil, name='perfil'),
    path('fotografos', views.fotografos, name='fotografos'),
    path('mensaje-enviado', views.mensaje_enviado, name='mensaje-enviado'),
    path('formulario', views.formulario, name='formulario'),
    path('solicitud-recibida', views.solicitud_recibida, name='solicitud-recibida'),
    path('wishlist', views.wishlist, name='wishlist'),
    path('historial', views.historial, name='historial'),
    path('contacto', views.contacto, name='contacto'),
    path('prueba2', views.prueba, name='prueba2'),
    path('payment', views.payment, name='payment'),
    path('stripe', views.stripe_log, name='stripe'),

    # PAGINAS DE INFORMACION DEL FOOTER
    path('terms', views.terms, name='terms'),
    path('privacy-policy', views.privacy, name='privacy'),
    path('taxes', views.taxes, name='taxes'),
    path('free-sub', views.free_sub, name='free-sub'),
    path('copyright', views.copyright, name='copyright'),
    path('secure-payments', views.secure_payments, name='secure-payments'),
    path('manual', views.manual, name='manual'),
    path('how-does-it-work', views.how_does_it_work, name='how-does-it-work'),
    path('devolucion', views.devolucion, name='devolucion'),
]
