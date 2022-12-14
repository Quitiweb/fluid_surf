# Generated by Django 2.2.6 on 2019-10-09 13:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('home', '0007_compra'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='compra',
            name='user',
        ),
        migrations.AddField(
            model_name='compra',
            name='comprador',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, related_name='compra_c', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='compra',
            name='vendedor',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, related_name='compra_v', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='compra',
            name='producto',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, related_name='compra_p', to='home.Producto'),
        ),
    ]
