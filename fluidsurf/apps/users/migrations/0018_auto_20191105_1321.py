# Generated by Django 2.2.6 on 2019-11-05 12:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0017_auto_20191023_1229'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='zona',
            field=models.CharField(choices=[('Europe', 'Europe'), ('Africa', 'Africa'), ('Asia', 'Asia'), ('Oceania', 'Oceania'), ('North America', 'North America'), ('South America', 'South America')], default='EU', max_length=50),
        ),
    ]
