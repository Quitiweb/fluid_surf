# Generated by Django 2.1.9 on 2019-09-26 13:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0003_auto_20190925_1622'),
    ]

    operations = [
        migrations.AddField(
            model_name='producto',
            name='imagen1',
            field=models.ImageField(blank=True, upload_to='img/productos/'),
        ),
        migrations.AddField(
            model_name='producto',
            name='imagen2',
            field=models.ImageField(blank=True, upload_to='img/productos/'),
        ),
        migrations.AddField(
            model_name='producto',
            name='imagen3',
            field=models.ImageField(blank=True, upload_to='img/productos/'),
        ),
        migrations.AddField(
            model_name='producto',
            name='imagen4',
            field=models.ImageField(blank=True, upload_to='img/productos/'),
        ),
        migrations.AddField(
            model_name='producto',
            name='imagen5',
            field=models.ImageField(blank=True, upload_to='img/productos/'),
        ),
        migrations.AddField(
            model_name='producto',
            name='imagen6',
            field=models.ImageField(blank=True, upload_to='img/productos/'),
        ),
        migrations.AddField(
            model_name='producto',
            name='imagen7',
            field=models.ImageField(blank=True, upload_to='img/productos/'),
        ),
        migrations.AddField(
            model_name='producto',
            name='imagen8',
            field=models.ImageField(blank=True, upload_to='img/productos/'),
        ),
        migrations.AddField(
            model_name='producto',
            name='imagen9',
            field=models.ImageField(blank=True, upload_to='img/productos/'),
        ),
    ]