from django.contrib import admin

from .models import Solicitud, Target, Mercado, Servicios, Articulo, Alquiler, Coleccion, GaleriaArticulo, Categoria, \
    Maestro, VarianteArticulo, DefinicionVariante, PropuestaComercial, Marca, Espacio, Promocion, EstiloVida, Conexion, \
    CarritoItem, Carrito, Pedido, PuntoDeVenta, ArticuloPDV, Notificacion


class CustomMarca(admin.ModelAdmin):
    list_display = ['user', 'is_online', 'is_mayorista', 'is_marketplaces', ]


admin.site.register(Solicitud)
admin.site.register(Target)
admin.site.register(Mercado)
admin.site.register(EstiloVida)
admin.site.register(Servicios)
admin.site.register(Articulo)
admin.site.register(Alquiler)
admin.site.register(Coleccion)
admin.site.register(PropuestaComercial)
admin.site.register(PuntoDeVenta)
admin.site.register(Conexion)
admin.site.register(GaleriaArticulo)
admin.site.register(Categoria)
admin.site.register(Maestro)
admin.site.register(VarianteArticulo)
admin.site.register(DefinicionVariante)
admin.site.register(Marca, CustomMarca)
admin.site.register(Espacio)
admin.site.register(Promocion)
admin.site.register(Carrito)
admin.site.register(CarritoItem)
admin.site.register(Pedido)
admin.site.register(ArticuloPDV)
admin.site.register(Notificacion)
