# Generated by Django 2.0 on 2018-04-21 17:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contributors', '0014_auto_20180405_1626'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contributor',
            name='byline_photo',
            field=models.ForeignKey(
                blank=True,
                help_text='photo used for byline credit.',
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name='person',
                to='photo.ImageFile'
            ),
        ),
    ]
