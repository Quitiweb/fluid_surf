# Generated by Django 2.1.9 on 2019-08-23 08:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='validado',
            field=models.BooleanField(blank=True, default=False),
        ),
    ]
