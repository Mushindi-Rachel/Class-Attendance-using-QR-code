# Generated by Django 4.2 on 2024-09-12 08:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mysite', '0007_rename_year_unit_academic_year'),
    ]

    operations = [
        migrations.RenameField(
            model_name='semester',
            old_name='name',
            new_name='semester',
        ),
    ]