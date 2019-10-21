from django.contrib.auth.models import AbstractUser
from django.core.files.storage import FileSystemStorage
from django.db import models
from django.core.validators import RegexValidator, validate_comma_separated_integer_list

from ..payments.managers import UserManager
from django.utils.translation import ugettext_lazy as _
from ..helpers.helper import ANTG1, ANTIGUEDAD, FACT1, FACTURACION


class CustomUser(AbstractUser):
    SURFERO = 'SURFERO'
    FOTOGRAFO = 'FOTOGRAFO'
    ADMIN = 'ADMIN'

    USER = (
        (SURFERO, 'Surfero'),
        (FOTOGRAFO, 'Fotografo'),
        (ADMIN, 'Admin'),
    )

    AREA_CHOICES = (
        ('EU', _("Europe")),
        ('AF', _("Africa")),
        ('AS', _("Asia")),
        ('OC', _("Oceania")),
        ('NA', _("North America")),
        ('SA', _("South America"))
    )

    tipo_de_usuario = models.CharField(
        max_length=15,
        choices=USER,
        default=SURFERO,
    )

    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Formato: '+999999999'. Max 15 dígitos.")
    telefono = models.CharField(validators=[phone_regex], max_length=17, blank=True)  # validators should be a list
    pais = models.CharField(max_length=50, default="")
    zona = models.CharField(
        max_length=50,
        choices=AREA_CHOICES,
        default='EU'
    )

    validado = models.BooleanField(default=False)

    alias = models.CharField(max_length=25, default='', blank=True)
    CV = models.TextField(max_length=200, blank=True)
    profile_pic = models.ImageField(upload_to="img/photographer/", blank=True)
    main_pic = models.ImageField(upload_to="img/photographer/", blank=True)

    wishlist = models.CharField(validators=[validate_comma_separated_integer_list], max_length=500, default='', blank=True)

    objects = UserManager()

    def __str__(self):
        return self.username
