# Generated by Django 5.1.1 on 2024-09-12 22:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gameinfo', '0020_extra_info_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='extra_info',
            name='image',
        ),
        migrations.CreateModel(
            name='Artwork',
            fields=[
                ('artwork_id', models.IntegerField(primary_key=True, serialize=False)),
                ('image', models.ImageField(blank=True, null=True, upload_to='')),
                ('game_infos', models.ManyToManyField(to='gameinfo.game_info')),
            ],
        ),
        migrations.CreateModel(
            name='Screenshots',
            fields=[
                ('screen_shot_id', models.IntegerField(primary_key=True, serialize=False)),
                ('image', models.ImageField(blank=True, null=True, upload_to='')),
                ('game_infos', models.ManyToManyField(to='gameinfo.game_info')),
            ],
        ),
    ]
