# Generated by Django 4.2 on 2024-09-09 09:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mysite', '0006_alter_semester_name'),
    ]

    operations = [
        migrations.RenameField(
            model_name='unit',
            old_name='year',
            new_name='academic_year',
        ),
    ]
