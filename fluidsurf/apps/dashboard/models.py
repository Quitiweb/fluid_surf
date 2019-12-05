import datetime

from django.db import models

# Create your models here.
class RegistroCompras(models.Model):
    compras = models.CharField(max_length=10)

    fecha = models.DateField()

    def __str__(self):
        return 'Registro-' + str(self.fecha)

