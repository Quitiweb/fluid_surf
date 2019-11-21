# Generated by Django 2.2.6 on 2019-11-05 12:57

from django.db import migrations
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0027_privacy'),
    ]

    operations = [
        migrations.AlterField(
            model_name='terms',
            name='text',
            field=tinymce.models.HTMLField(default='Terminos y condiciones de uso...', help_text='Este es el texto que aparecera en la seccion terminos y condiciones', max_length=45000),
        ),
    ]