# Generated by Django 1.11 on 2017-09-27 13:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion

import apps.contributors.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('contributors', '0010_auto_20151013_2307'),
    ]

    operations = [
        migrations.AddField(
            model_name='contributor',
            name='user',
            field=models.OneToOneField(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL
            ),
        ),
        migrations.AddField(
            model_name='position',
            name='is_management',
            field=models.BooleanField(
                default=False,
                help_text='Is this a management position',
                verbose_name='is management'
            ),
        ),
        migrations.AlterField(
            model_name='position',
            name='groups',
            field=models.ManyToManyField(
                help_text='Implicit auth Group membership',
                to='auth.Group',
                verbose_name='groups'
            ),
        ),
        migrations.AlterField(
            model_name='position',
            name='title',
            field=models.CharField(
                help_text='Job title at the publication.',
                max_length=50,
                unique=True,
                verbose_name='title'
            ),
        ),
        migrations.AlterField(
            model_name='stint',
            name='contributor',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to='contributors.Contributor',
                verbose_name='contributor'
            ),
        ),
        migrations.AlterField(
            model_name='stint',
            name='end_date',
            field=models.DateField(
                blank=True, null=True, verbose_name='end date'
            ),
        ),
        migrations.AlterField(
            model_name='stint',
            name='position',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to='contributors.Position',
                verbose_name='position'
            ),
        ),
        migrations.AlterField(
            model_name='stint',
            name='start_date',
            field=models.DateField(
                default=apps.contributors.models.today,
                verbose_name='start date'
            ),
        ),
    ]
