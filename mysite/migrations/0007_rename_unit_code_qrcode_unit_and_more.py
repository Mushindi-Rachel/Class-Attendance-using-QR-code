# Generated by Django 4.2 on 2024-03-06 13:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mysite', '0006_rename_date_qrcode_lecture_date_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='qrcode',
            old_name='unit_code',
            new_name='unit',
        ),
        migrations.AlterField(
            model_name='qrcode',
            name='qr_code_image',
            field=models.ImageField(blank=True, null=True, upload_to='qr_codes/'),
        ),
    ]
