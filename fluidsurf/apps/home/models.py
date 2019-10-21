import datetime

from django.db import models
from django.utils.translation import ugettext_lazy as _

from fluidsurf.apps.users.models import CustomUser
from django_google_maps.fields import AddressField, GeoLocationField

AREA_CHOICES = (
    ('EU', _("Europe")),
    ('AF', _("Africa")),
    ('AS', _("Asia")),
    ('OC', _("Oceania")),
    ('NA', _("North America")),
    ('AS', _("South America"))
)


class Producto(models.Model):
    id = models.AutoField(primary_key=True)

    nombre = models.CharField(max_length=100)
    precio = models.IntegerField()

    fecha = models.DateField()
    spot = models.CharField(max_length=25, choices=AREA_CHOICES, default='EU')

    descripcion = models.CharField(max_length=50, blank=True)

    imagen0 = models.ImageField(upload_to="img/productos/", blank=True)
    imagen1 = models.ImageField(upload_to="img/productos/", blank=True)
    imagen2 = models.ImageField(upload_to="img/productos/", blank=True)
    imagen3 = models.ImageField(upload_to="img/productos/", blank=True)
    imagen4 = models.ImageField(upload_to="img/productos/", blank=True)
    imagen5 = models.ImageField(upload_to="img/productos/", blank=True)
    imagen6 = models.ImageField(upload_to="img/productos/", blank=True)
    imagen7 = models.ImageField(upload_to="img/productos/", blank=True)
    imagen8 = models.ImageField(upload_to="img/productos/", blank=True)
    imagen9 = models.ImageField(upload_to="img/productos/", blank=True)

    stock = models.IntegerField(default=1)

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='producto')

    def __str__(self):
        return self.nombre


class Compra(models.Model):
    comprador = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='compra_c', default='')
    vendedor = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='compra_v', default='')
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name='compra_p', default='')
    fecha = models.DateField()

    def __str__(self):
        return str(self.vendedor) + "-" + str(self.comprador) + str(self.fecha)


class Ubicacion(models.Model):
    spot = models.CharField(max_length=25, choices=AREA_CHOICES, default='Europa')
    geoloc = GeoLocationField(blank=True)

    def __str__(self):
        return self.spot

    class Meta:
        verbose_name = 'Ubicacion'
        verbose_name_plural = 'Ubicaciones'


class Denuncia(models.Model):
    CHOICES = (
        ('MAL USO', _("Bad usage of the app")),
        ('INAPROPIADO', _("Innapropiate content")),
        ('SPAM', _("Spam")),
        ('OTRO', _("Other")),
    )

    emisor = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='denuncia_e', default='')
    receptor = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='denuncia_r', default='')
    motivo = models.CharField(max_length=30, choices=CHOICES, default='MAL USO')
    detalles = models.CharField(max_length=200)

    def __str__(self):
        return self.receptor.username + '-' + self.emisor.username + '-' + str(datetime.date.today())
