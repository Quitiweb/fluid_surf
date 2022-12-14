# Generated by Django 2.2.6 on 2019-11-05 12:56

from django.db import migrations, models
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0026_terms'),
    ]

    operations = [
        migrations.CreateModel(
            name='Privacy',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=200)),
                ('text', tinymce.models.HTMLField(default='Politica de privacidad...', help_text='Este es el texto que aparecera en la seccion politica de privacidad', max_length=15000)),
            ],
            options={
                'verbose_name_plural': 'Politica de Privacidad',
            },
        ),
    ]
