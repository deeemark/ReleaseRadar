# Generated by Django 5.1.1 on 2024-09-12 22:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gameinfo', '0021_remove_extra_info_image_artwork_screenshots'),
    ]

    operations = [
        migrations.RenameField(
            model_name='screenshots',
            old_name='screen_shot_id',
            new_name='screenshot_id',
        ),
    ]
