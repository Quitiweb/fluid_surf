# Generated by Django 2.2.6 on 2019-10-04 07:40

from django.db import migrations, models
import django_google_maps.fields


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0005_auto_20190926_1537'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ubicacion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('direccion', django_google_maps.fields.AddressField(max_length=100)),
                ('geoloc', django_google_maps.fields.GeoLocationField(blank=True, max_length=100)),
            ],
        ),
    ]
