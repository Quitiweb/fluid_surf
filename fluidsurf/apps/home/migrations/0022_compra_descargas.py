# Generated by Django 2.1.9 on 2019-10-23 10:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0021_auto_20191021_1500'),
    ]

    operations = [
        migrations.AddField(
            model_name='compra',
            name='descargas',
            field=models.IntegerField(default=0),
        ),
    ]
