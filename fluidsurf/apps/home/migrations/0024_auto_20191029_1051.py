# Generated by Django 2.2.6 on 2019-10-29 09:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0023_auto_20191023_1230'),
    ]

    operations = [
        migrations.AlterField(
            model_name='producto',
            name='spot',
            field=models.CharField(choices=[('Europe', 'Europe'), ('Africa', 'Africa'), ('Asia', 'Asia'), ('Oceania', 'Oceania'), ('North America', 'North America'), ('South America', 'South America')], default='EU', max_length=25),
        ),
        migrations.AlterField(
            model_name='ubicacion',
            name='spot',
            field=models.CharField(choices=[('Europe', 'Europe'), ('Africa', 'Africa'), ('Asia', 'Asia'), ('Oceania', 'Oceania'), ('North America', 'North America'), ('South America', 'South America')], default='Europa', max_length=25),
        ),
    ]