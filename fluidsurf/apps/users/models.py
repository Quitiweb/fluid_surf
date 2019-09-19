from django.contrib.auth.models import AbstractUser
from django.core.files.storage import FileSystemStorage
from django.db import models
from django.core.validators import RegexValidator

from ..payments.managers import UserManager
from ..helpers.helper import ANTG1, ANTIGUEDAD, FACT1, FACTURACION


class OverwriteStorage(FileSystemStorage):
    def get_available_name(self, name, max_length=None):
        self.delete(name)
        return name


def upload_to_logo(instance, filename):
    new_filename = str(instance.id) + '.' + 'jpg'
    return 'img/logo/%s' % new_filename


def upload_to_perfil(instance, filename):
    new_filename = str(instance.id) + '.' + 'jpg'
    return 'img/perfil/%s' % new_filename


class CustomUser(AbstractUser):
    SURFERO = 'SURFERO'
    FOTOGRAFO = 'FOTOGRAFO'
    ADMIN = 'ADMIN'

    USER = (
        (SURFERO, 'Surfero'),
        (FOTOGRAFO, 'Fotografo'),
        (ADMIN, 'Admin'),
    )

    tipo_de_usuario = models.CharField(
        max_length=15,
        choices=USER,
        default=SURFERO,
    )

    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Formato: '+999999999'. Max 15 dígitos.")
    telefono = models.CharField(validators=[phone_regex], max_length=17, blank=True)  # validators should be a list
    pais = models.CharField(max_length=50, default="")
    zona = models.CharField(max_length=50, default="")
    is_empresa = models.BooleanField(default=False, blank=True)
    is_autonomo = models.BooleanField(default=False, blank=True)
    is_marca = models.BooleanField(default=False, blank=True)
    is_espacio = models.BooleanField(default=False, blank=True)

    titular = models.CharField(max_length=50, blank=False, default='')
    sobre_mi_negocio = models.CharField(max_length=500, blank=False, default='')

    logo = models.ImageField(upload_to=upload_to_logo, default='', storage=OverwriteStorage(), blank=True, null=True)
    foto_perfil = models.ImageField(upload_to=upload_to_perfil, storage=OverwriteStorage(), blank=True, null=True)

    facebook = models.URLField(default='', blank=True)
    linkedin = models.URLField(default='', blank=True)
    youtube = models.URLField(default='', blank=True)
    twitter = models.URLField(default='', blank=True)

    validado = models.BooleanField(default=False)

    objects = UserManager()

    def __str__(self):
        return self.username


class GaleriaUsuario(models.Model):
    imagen = models.ImageField(upload_to="img/galeria/", blank=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='galeria')


class Comentario(models.Model):
    autor = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='autor')
    para = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='para_mi')
    puntuacion = models.FloatField(default=5, blank=True)
    contenido = models.TextField()

    def save(self, *args, **kwargs):
        perfil_destino = MiPerfil.objects.get(user=self.para)
        valoraciones = perfil_destino.user.para_mi.all()
        perfil_destino.puntuacion = (perfil_destino.puntuacion + self.puntuacion) / (valoraciones.count() + 1)
        perfil_destino.puntuacion = round(perfil_destino.puntuacion * 2) / 2
        perfil_destino.save()
        super(Comentario, self).save(*args, **kwargs)


class Empresa(models.Model):
    razon_social = models.CharField(max_length=60)
    nif = models.CharField(max_length=25, blank=True)

    antiguedad = models.CharField(
        max_length=50,
        choices=ANTIGUEDAD,
        default=ANTG1,
        blank=True,
    )
    facturacion = models.CharField(
        max_length=50,
        choices=FACTURACION,
        default=FACT1,
        blank=True,
    )

    iva = models.CharField(max_length=15, blank=True)

    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="empresa"
    )


class Autonomo(models.Model):
    irpf = models.CharField(max_length=25, blank=True)
    razon_social = models.CharField(max_length=60)
    nif = models.CharField(max_length=25, blank=True)

    antiguedad = models.CharField(
        max_length=50,
        choices=ANTIGUEDAD,
        default=ANTG1,
        blank=True,
    )
    facturacion = models.CharField(
        max_length=50,
        choices=FACTURACION,
        default=FACT1,
        blank=True,
    )

    iva = models.CharField(max_length=15, blank=True)

    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="autonomo"
    )

    def __str__(self):
        return self.razon_social


class MiPerfil(models.Model):
    direccion = models.CharField(max_length=100, default='', blank=True)
    cp = models.CharField(max_length=8, default='', blank=True)
    ciudad = models.CharField(max_length=20, default='', blank=True)
    pais = models.CharField(max_length=20, default='', blank=True)
    ventas = models.IntegerField(default=0)
    negociable = models.BooleanField(default=False)
    is_marca = models.BooleanField(default=False)
    is_espacio = models.BooleanField(default=False)
    puntuacion = models.FloatField(default=0, blank=True)
    lat = models.FloatField(blank=True, null=True)
    lng = models.FloatField(blank=True, null=True)

    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='perfil'
    )

    def __init__(self, *args, **kwargs):
        super(MiPerfil, self).__init__(*args, **kwargs)
        self.old_is_marca = getattr(self, 'is_marca')
        self.old_is_espacio = getattr(self, 'is_espacio')

    def save(self, *args, **kwargs):
        if self.old_is_marca and self.is_espacio:
            self.is_marca = False
        elif self.old_is_espacio and self.is_marca:
            self.is_espacio = False
        super(MiPerfil, self).save(*args, **kwargs)

    def __str__(self):
        return 'Perfil de ' + self.user.username

    class Meta:
        verbose_name_plural = 'Perfiles'
