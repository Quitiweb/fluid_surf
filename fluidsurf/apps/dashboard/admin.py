from django.contrib import admin

# Register your models here.
from fluidsurf.apps.dashboard.models import RegistroCompras, RegistroFotografos, RegistroSurferos

admin.site.register(RegistroCompras)
admin.site.register(RegistroFotografos)
admin.site.register(RegistroSurferos)