# Generated by Django 2.1.9 on 2019-09-18 15:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20190916_1619'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='tipo_de_usuario',
            field=models.CharField(choices=[('SURFERO', 'Surfero'), ('FOTOGRAFO', 'Fotografo'), ('ADMIN', 'Admin')], default='SURFERO', max_length=15),
        ),
    ]
