from django.core.management import call_command
from django.db import migrations

FIXTURE = 'ad_formats'


def load_fixture(apps, schema_editor):
    call_command('loaddata', FIXTURE, app_label='adverts')


def unload_fixture(apps, schema_editor):
    MyModel = apps.get_model('adverts', 'AdFormat')
    MyModel.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ('adverts', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(
            code=load_fixture,
            reverse_code=unload_fixture,
        ),
    ]
