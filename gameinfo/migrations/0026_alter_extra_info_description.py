# Generated by Django 5.1.1 on 2024-09-14 06:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gameinfo', '0025_alter_extra_info_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='extra_info',
            name='description',
            field=models.CharField(max_length=5000),
        ),
    ]
