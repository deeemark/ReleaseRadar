# Generated by Django 5.1 on 2024-09-08 17:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gameinfo', '0017_alter_release_time_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='extra_info',
            name='description',
            field=models.CharField(max_length=5000),
        ),
    ]
