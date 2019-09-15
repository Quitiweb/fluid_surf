from django.urls import path

from . import views

# Comentario de Rafa: Esto por que esta aqui??
# Viene arrastrado desde el blog que tambien lo tiene incluido
# app_name = 'noticias'

urlpatterns = [
    path('', views.noticias, name='noticias'),
    path(r'<int:year>/<int:month>/<int:day>/<slug:slug>', views.Single.as_view(), name='single'),
]
