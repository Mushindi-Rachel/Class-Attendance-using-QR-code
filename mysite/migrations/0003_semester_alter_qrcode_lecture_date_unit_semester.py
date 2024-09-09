# Generated by Django 4.2 on 2024-09-06 14:51

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('mysite', '0002_alter_studentprofile_gender'),
    ]

    operations = [
        migrations.CreateModel(
            name='Semester',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(choices=[('Jan-Apr', 'January-April'), ('May-Aug', 'May-August'), ('Sep-Dec', 'September-December')], max_length=15, unique=True)),
            ],
        ),
        migrations.AlterField(
            model_name='qrcode',
            name='lecture_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='unit',
            name='semester',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='mysite.semester'),
        ),
    ]