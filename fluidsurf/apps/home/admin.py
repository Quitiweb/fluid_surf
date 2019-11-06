from django.contrib import admin
from django.contrib.auth.admin import UserAdmin


from .models import Producto, Compra, Ubicacion, Denuncia, Terms, Privacy, Taxes, FreeSub, SecurePayments, Copyright, \
    Manual

admin.site.register(Producto)
admin.site.register(Compra)
admin.site.register(Ubicacion)
admin.site.register(Denuncia)

admin.site.register(Terms)
admin.site.register(Privacy)
admin.site.register(Taxes)
admin.site.register(FreeSub)
admin.site.register(Copyright)
admin.site.register(SecurePayments)
admin.site.register(Manual)
