# Generated by Django 1.10 on 2016-09-24 19:28

from django.db import migrations, models

import apps.issues.models


class Migration(migrations.Migration):

    dependencies = [
        ('issues', '0009_auto_20160906_1614'),
    ]

    operations = [
        migrations.AlterField(
            model_name='issue',
            name='publication_date',
            field=models.DateField(
                blank=True, default=apps.issues.models.today, null=True
            ),
        ),
        migrations.AlterField(
            model_name='printissue',
            name='pdf',
            field=models.FileField(
                help_text='Pdf file for this issue.',
                upload_to=apps.issues.models.upload_pdf_to
            ),
        ),
    ]
