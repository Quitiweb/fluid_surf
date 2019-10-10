from django.urls import path

from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('productos', views.productos, name='productos'),
    path('compras', views.compras, name='compras'),
    path('usuarios', views.usuarios, name='usuarios'),
]
