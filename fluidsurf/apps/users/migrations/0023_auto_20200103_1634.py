# Generated by Django 2.1.9 on 2020-01-03 15:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0022_auto_20191226_1724'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='stripeuser',
            name='user',
        ),
        migrations.AddField(
            model_name='customuser',
            name='stripe_id',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.DeleteModel(
            name='StripeUser',
        ),
    ]
