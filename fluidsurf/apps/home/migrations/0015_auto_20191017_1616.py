# Generated by Django 2.1.9 on 2019-10-17 14:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0014_auto_20191016_1237'),
    ]

    operations = [
        migrations.AlterField(
            model_name='producto',
            name='spot',
            field=models.CharField(choices=[('EU', 'Europe'), ('AF', 'Africa'), ('Asia', 'Asia'), ('Oceania', 'Oceania'), ('America del Norte', 'North America'), ('America del Sur', 'South America')], default='Europa', max_length=25),
        ),
        migrations.AlterField(
            model_name='ubicacion',
            name='spot',
            field=models.CharField(choices=[('EU', 'Europe'), ('AF', 'Africa'), ('Asia', 'Asia'), ('Oceania', 'Oceania'), ('America del Norte', 'North America'), ('America del Sur', 'South America')], default='Europa', max_length=25),
        ),
    ]
