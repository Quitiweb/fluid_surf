# Generated by Django 2.2.6 on 2019-11-07 10:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('home', '0036_howdoesitwork'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductReturn',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reason', models.CharField(max_length=50)),
                ('is_opened', models.BooleanField(default=False)),
                ('details', models.TextField(max_length=200)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='return_o', to='home.Compra')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='return_u', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
