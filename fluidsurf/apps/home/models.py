import datetime

from django.db import models
from django.utils.translation import ugettext_lazy as _
from tinymce.models import HTMLField

from fluidsurf.apps.users.models import CustomUser
from django_google_maps.fields import AddressField, GeoLocationField

AREA_CHOICES = (
    ('Europe', _("Europe")),
    ('Africa', _("Africa")),
    ('Asia', _("Asia")),
    ('Oceania', _("Oceania")),
    ('North America', _("North America")),
    ('South America', _("South America"))
)

DEV_REASON_CHOICES = (
    ('Dead on Arrival', _("Dead on Arrival")),
    ('Faulty', _("Faulty, please supply details")),
    ('Order Error', _("Order Error")),
    ('Other', _("Other, please supply details")),
    ('Wrong Item', _("Received Wrong Item"))
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
    descargas = models.IntegerField(default=3)
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


# PAGINAS DE INFORMACION DEL FOOTER
class Terms(models.Model):
    text = HTMLField(max_length=45000,
                     default="Terminos y condiciones de uso...",
                     help_text="Este es el texto que aparecera en la seccion terminos y condiciones")

    text_en = HTMLField(max_length=45000,
                     default="Terms and conditions...",
                     help_text="This is the text that will appear on your terms and conditions section")
    class Meta:
        verbose_name_plural = 'Terminos y Condiciones'

    def __str__(self):
        return 'Terminos&Condiciones-' + str(datetime.date.today())


class Privacy(models.Model):
    text = HTMLField(max_length=45000,
                     default="Politica de privacidad...",
                     help_text="Este es el texto que aparecera en la seccion politica de privacidad")

    text_en = HTMLField(max_length=45000,
                     default="Privacy policy...",
                     help_text="This is the text that will appear on your policy privacy section")

    class Meta:
        verbose_name_plural = 'Politica de Privacidad'

    def __str__(self):
        return 'Politica de privacidad-' + str(datetime.date.today())


class Taxes(models.Model):
    text = HTMLField(max_length=45000,
                     default="Impuestos y facturacion...",
                     help_text="Este es el texto que aparecera en la seccion impuestos y facturacion")

    text_en = HTMLField(max_length=45000,
                     default="Taxes and billing...",
                     help_text="This is the text that will appear on your taxes & billing section")

    class Meta:
        verbose_name_plural = 'Impuestos y facturacion'

    def __str__(self):
        return 'ImpuestosyFacturacion-' + str(datetime.date.today())


class FreeSub(models.Model):
    text = HTMLField(max_length=45000,
                     default="Suscripcion gratuita...",
                     help_text="Este es el texto que aparecera en la seccion suscripcion gratuita")

    text_en = HTMLField(max_length=45000,
                        default="Free subscription features...",
                        help_text="This is the text that will appear on your free subcription features section")

    class Meta:
        verbose_name_plural = 'Suscripcion gratuita'

    def __str__(self):
        return 'Suscripciongratuita-' + str(datetime.date.today())


class Copyright(models.Model):
    text = HTMLField(max_length=45000,
                     default="Copyright, licencias y tamaños...",
                     help_text="Este es el texto que aparecera en la seccion copyright, licencias y tamaños")

    text_en = HTMLField(max_length=45000,
                        default="Copyright, licenses and sizes...",
                        help_text="This is the text that will appear on your copyright, licenses and sizes section")

    class Meta:
        verbose_name_plural = 'Copyright, licencias y tamaños'

    def __str__(self):
        return 'Copyright-' + str(datetime.date.today())


class SecurePayments(models.Model):

    image = models.ImageField(upload_to='img/information/', blank=True)

    text = HTMLField(max_length=45000,
                     default="Seguridad en pagos...",
                     help_text="Este es el texto que aparecera en la seccion seguridad en pagos")

    text_en = HTMLField(max_length=45000,
                        default="Secure payments...",
                        help_text="This is the text that will appear on your secure payments section")

    class Meta:
        verbose_name_plural = 'Seguridad en pagos'

    def __str__(self):
        return 'Seguridadenpagos-' + str(datetime.date.today())


class Manual(models.Model):
    text = HTMLField(max_length=45000,
                     default="Instrucciones: vender fotos...",
                     help_text="Este es el texto que aparecera en la seccion instrucciones: vender fotos")

    text_en = HTMLField(max_length=45000,
                        default="Selling photos: manual...",
                        help_text="This is the text that will appear on your selling photos: manual section")

    class Meta:
        verbose_name_plural = 'Instrucciones: vender fotos'

    def __str__(self):
        return 'Instrucciones-' + str(datetime.date.today())


class HowDoesItWork(models.Model):
    text = HTMLField(max_length=45000,
                     default="Como funciona...",
                     help_text="Este es el texto que aparecera en la seccion como funciona")

    text_en = HTMLField(max_length=45000,
                        default="How does it work...",
                        help_text="This is the text that will appear on your how does it work section")

    image = models.ImageField(upload_to='img/information/', blank=True)

    text2 = HTMLField(max_length=45000,
                     default="2 Como funciona...",
                     help_text="Este es el texto que aparecera en la seccion como funciona")

    text2_en = HTMLField(max_length=45000,
                        default=" How does it work...",
                        help_text="This is the text that will appear on your how does it work section")

    class Meta:
        verbose_name_plural = '¿Como funciona?'

    def __str__(self):
        return 'Comofunciona-' + str(datetime.date.today())


class Devolucion(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='return_u')
    product = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name='return_p')

    reason = models.CharField(max_length=50, choices=DEV_REASON_CHOICES)
    is_opened = models.BooleanField(default=False)

    details = models.TextField(max_length=200, blank=True)

    class Meta:
        verbose_name_plural = 'Devoluciones'

    def __str__(self):
        return self.user.username + "-" + self.product.nombre + "-" + str(datetime.date.today())


class WatermarkImage(models.Model):
    activo = models.BooleanField(
        default=False, blank=True, help_text=_("Ten activo solo uno al mismo tiempo")
    )

    imagen = models.ImageField(upload_to="img/watermark/", blank=False)

    def __str__(self):
        return 'Watermark-' + str(datetime.date.today())
