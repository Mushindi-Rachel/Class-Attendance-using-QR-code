# Generated by Django 4.2 on 2024-09-12 09:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mysite', '0008_rename_name_semester_semester'),
    ]

    operations = [
        migrations.RenameField(
            model_name='semester',
            old_name='semester',
            new_name='name',
        ),
    ]
