# Generated by Django 2.1.9 on 2020-04-20 15:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0045_auto_20200420_1303'),
    ]

    operations = [
        migrations.AlterField(
            model_name='producto',
            name='spot',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='producto_spot', to='home.Spot'),
        ),
    ]