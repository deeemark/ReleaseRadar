# Generated by Django 5.1 on 2024-09-08 05:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gameinfo', '0013_release_time_release_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='release_time',
            name='release_date',
        ),
    ]
