# Generated by Django 2.1.9 on 2019-09-25 14:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_auto_20190925_1558'),
    ]

    operations = [
        migrations.AddField(
            model_name='producto',
            name='nombre',
            field=models.CharField(default='producto', max_length=25),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='producto',
            name='precio',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
