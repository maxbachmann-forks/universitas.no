# Generated by Django 2.0 on 2018-04-12 21:18

import django.core.validators
from django.db import migrations
import sorl.thumbnail.fields

import apps.photo.models


class Migration(migrations.Migration):

    dependencies = [
        ('photo', '0021_auto_20180412_1610'),
    ]

    operations = [
        migrations.RenameField('imagefile', 'source_file', 'original'),
        migrations.AlterField(
            model_name='imagefile',
            name='original',
            field=sorl.thumbnail.fields.ImageField(
                height_field='full_height',
                max_length=1024,
                upload_to=apps.photo.models.upload_image_to,
                validators=[
                    django.core.validators.FileExtensionValidator([
                        'jpg', 'jpeg', 'png'
                    ])
                ],
                verbose_name='original',
                width_field='full_width'
            ),
            preserve_default=True,
        ),
    ]
