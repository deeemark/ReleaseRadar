# Generated by Django 5.1 on 2024-09-08 05:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gameinfo', '0015_release_time_date'),
    ]

    operations = [
        migrations.RenameField(
            model_name='release_time',
            old_name='release_season',
            new_name='season',
        ),
    ]
