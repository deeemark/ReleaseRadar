# Generated by Django 5.1 on 2024-09-10 20:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gameinfo', '0018_alter_extra_info_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='hype',
            name='average_hype',
            field=models.IntegerField(default=0),
        ),
    ]
