from django.db import models

from ..users.models import CustomUser


class Seller(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    stripe_user_id = models.CharField(max_length=255, blank=True)
    stripe_access_token = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.user.email
