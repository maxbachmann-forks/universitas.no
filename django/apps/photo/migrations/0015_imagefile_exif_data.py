# Generated by Django 1.11 on 2017-09-26 23:37

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('photo', '0014_auto_20170920_1826'),
    ]

    operations = [
        migrations.AddField(
            model_name='imagefile',
            name='exif_data',
            field=django.contrib.postgres.fields.jsonb.JSONField(
                default=dict,
                help_text='exif_data',
                verbose_name='exif_data',
            ),
        ),
    ]
