# Generated by Django 2.1.9 on 2019-09-02 22:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('landing', '0018_merge_20190903_0033'),
    ]

    operations = [
        migrations.AddField(
            model_name='puntodeventa',
            name='activo',
            field=models.BooleanField(default=False),
        ),
    ]
