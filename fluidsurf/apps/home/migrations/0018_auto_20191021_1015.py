# Generated by Django 2.1.9 on 2019-10-21 08:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0017_denuncia'),
    ]

    operations = [
        migrations.AlterField(
            model_name='producto',
            name='spot',
            field=models.CharField(choices=[('EU', 'Europe'), ('AF', 'Africa'), ('AS', 'Asia'), ('OC', 'Oceania'), ('NA', 'North America'), ('AS', 'South America')], default='EU', max_length=25),
        ),
        migrations.AlterField(
            model_name='ubicacion',
            name='spot',
            field=models.CharField(choices=[('EU', 'Europe'), ('AF', 'Africa'), ('AS', 'Asia'), ('OC', 'Oceania'), ('NA', 'North America'), ('AS', 'South America')], default='Europa', max_length=25),
        ),
    ]
