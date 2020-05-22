# Generated by Django 2.1.9 on 2020-05-22 09:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('dashboard', '0003_auto_20191205_1506'),
    ]

    operations = [
        migrations.AddField(
            model_name='registrocompras',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_registro', to=settings.AUTH_USER_MODEL),
        ),
    ]