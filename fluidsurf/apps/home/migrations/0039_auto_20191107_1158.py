# Generated by Django 2.2.6 on 2019-11-07 10:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0038_auto_20191107_1154'),
    ]

    operations = [
        migrations.AlterField(
            model_name='devolucion',
            name='reason',
            field=models.CharField(choices=[('Dead on Arrival', 'Dead on Arrival'), ('Faulty', 'Faulty, please supply details'), ('Order Error', 'Order Error'), ('Other', 'Other, please supply details'), ('Wrong Item', 'Received Wrong Item')], max_length=50),
        ),
    ]