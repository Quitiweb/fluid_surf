from django.contrib import admin
from django.contrib.auth.admin import UserAdmin


from .models import Producto, Compra, Ubicacion, Denuncia

admin.site.register(Producto)
admin.site.register(Compra)
admin.site.register(Ubicacion)
admin.site.register(Denuncia)
