from django.contrib import admin
from django.contrib.auth.admin import UserAdmin


from .models import Producto, Compra, Denuncia, Terms, Privacy, Taxes, FreeSub, SecurePayments, Copyright, \
    Manual, HowDoesItWork, Devolucion, WatermarkImage, SolicitudStock, Continente, Pais, Area, Spot

admin.site.register(Producto)
admin.site.register(Compra)
admin.site.register(Denuncia)

admin.site.register(Terms)
admin.site.register(Privacy)
admin.site.register(Taxes)
admin.site.register(FreeSub)
admin.site.register(Copyright)
admin.site.register(SecurePayments)
admin.site.register(Manual)
admin.site.register(HowDoesItWork)
admin.site.register(Devolucion)
admin.site.register(WatermarkImage)
admin.site.register(SolicitudStock)

admin.site.register(Continente)
admin.site.register(Pais)
admin.site.register(Area)
admin.site.register(Spot)

