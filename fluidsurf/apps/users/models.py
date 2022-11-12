from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator, validate_comma_separated_integer_list

from ..payments.managers import UserManager


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

    stripe_id = models.CharField(max_length=100, blank=True)

    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$', message="Formato: '+999999999'. Max 15 dígitos.")

    # validators should be a list
    telefono = models.CharField(validators=[phone_regex], max_length=17, blank=True)

    pais = models.ForeignKey(
        'home.Pais', on_delete=models.CASCADE, related_name='u_pais', null=True, blank=True)

    validado = models.BooleanField(default=False)

    alias = models.CharField(max_length=25, default='', blank=True)
    CV = models.TextField(max_length=200, blank=True)
    profile_pic = models.ImageField(upload_to="img/photographer/", blank=True)
    main_pic = models.ImageField(upload_to="img/photographer/", blank=True)

    wishlist = models.CharField(
        validators=[validate_comma_separated_integer_list], max_length=500,
        default='', blank=True
    )

    objects = UserManager()

    def __str__(self):
        return self.username
