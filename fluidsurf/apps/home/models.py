from django.db import models

from fluidsurf.apps.users.models import CustomUser


class Producto(models.Model):
    fecha = models.DateField()
    spot = models.CharField(max_length=25)

    imagen0 = models.ImageField(upload_to="img/productos/", blank=True)
    # imagen1 = models.ImageField(upload_to="img/productos/", blank=True)
    # imagen2 = models.ImageField(upload_to="img/productos/", blank=True)
    # imagen3 = models.ImageField(upload_to="img/productos/", blank=True)
    # imagen4 = models.ImageField(upload_to="img/productos/", blank=True)
    # imagen5 = models.ImageField(upload_to="img/productos/", blank=True)
    # imagen6 = models.ImageField(upload_to="img/productos/", blank=True)
    # imagen7 = models.ImageField(upload_to="img/productos/", blank=True)
    # imagen8 = models.ImageField(upload_to="img/productos/", blank=True)
    # imagen9 = models.ImageField(upload_to="img/productos/", blank=True)

    stock = models.IntegerField(default=1)

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='producto')