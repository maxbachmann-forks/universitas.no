from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('issues', '0005_data_link_pdf_to_issue'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='printissue',
            name='publication_date',
        ),
        migrations.AlterField(
            model_name='printissue',
            name='issue',
            field=models.ForeignKey(
                on_delete=models.CASCADE,
                to='issues.Issue',
                related_name='pdfs',
                null=True
            ),
        ),
    ]
