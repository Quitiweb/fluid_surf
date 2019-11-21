# Generated by Django 2.2.6 on 2019-11-06 09:16

from django.db import migrations
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0029_auto_20191105_1359'),
    ]

    operations = [
        migrations.AddField(
            model_name='privacy',
            name='text_en',
            field=tinymce.models.HTMLField(default='Privacy policy...', help_text='This is the text that will appear on your policy privacy section', max_length=45000),
        ),
        migrations.AddField(
            model_name='terms',
            name='text_en',
            field=tinymce.models.HTMLField(default='Terms and conditions...', help_text='This is the text that will appear on your terms and conditions section', max_length=45000),
        ),
    ]