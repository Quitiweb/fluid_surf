# Generated by Django 2.2.6 on 2019-11-06 11:09

from django.db import migrations, models
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0035_manual'),
    ]

    operations = [
        migrations.CreateModel(
            name='HowDoesItWork',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', tinymce.models.HTMLField(default='Como funciona...', help_text='Este es el texto que aparecera en la seccion como funciona', max_length=45000)),
                ('text_en', tinymce.models.HTMLField(default='How does it work...', help_text='This is the text that will appear on your how does it work section', max_length=45000)),
                ('image', models.ImageField(blank=True, upload_to='img/information/')),
                ('text2', tinymce.models.HTMLField(default='2 Como funciona...', help_text='Este es el texto que aparecera en la seccion como funciona', max_length=45000)),
                ('text2_en', tinymce.models.HTMLField(default=' How does it work...', help_text='This is the text that will appear on your how does it work section', max_length=45000)),
            ],
            options={
                'verbose_name_plural': '¿Como funciona?',
            },
        ),
    ]
