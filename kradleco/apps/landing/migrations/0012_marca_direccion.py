# Generated by Django 2.1.9 on 2019-08-27 08:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('landing', '0011_articulopdv_coleccion'),
    ]

    operations = [
        migrations.AddField(
            model_name='marca',
            name='direccion',
            field=models.CharField(blank=True, default='', max_length=100),
        ),
    ]
