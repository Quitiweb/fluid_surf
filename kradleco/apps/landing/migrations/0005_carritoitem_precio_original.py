# Generated by Django 2.1.9 on 2019-08-09 09:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('landing', '0004_carrito_items_promo'),
    ]

    operations = [
        migrations.AddField(
            model_name='carritoitem',
            name='precio_original',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=8, null=True),
        ),
    ]
