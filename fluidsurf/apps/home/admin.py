from django.contrib import admin
from django.contrib.auth.admin import UserAdmin


from .models import Producto, Ubicacion

admin.site.register(Producto)
admin.site.register(Ubicacion)
