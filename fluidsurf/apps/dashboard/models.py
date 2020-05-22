
from django.db import models

# Create your models here.



class RegistroCompras(models.Model):
    compras = models.CharField(max_length=10)

    fecha = models.DateField()

    user = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE, related_name='user_registro', null=True)

    def __str__(self):
        return 'RegistroCompras-' + str(self.fecha)

    class Meta:
        verbose_name_plural = 'Registros de Compras'


class RegistroFotografos(models.Model):
    users = models.CharField(max_length=10)

    fecha = models.DateField()

    def __str__(self):
        return 'RegistroFotografos-' + str(self.fecha)

    class Meta:
        verbose_name_plural = 'Registros de Fotografos'


class RegistroSurferos(models.Model):
    users = models.CharField(max_length=10)

    fecha = models.DateField()

    def __str__(self):
        return 'RegistroSurferos-' + str(self.fecha)

    class Meta:
        verbose_name_plural = 'Registros de Surferos'

