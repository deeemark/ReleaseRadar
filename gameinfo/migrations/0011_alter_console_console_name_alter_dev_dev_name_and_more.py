# Generated by Django 5.1 on 2024-09-08 02:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gameinfo', '0010_alter_dev_dev_id_alter_genre_genre_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='console',
            name='console_name',
            field=models.CharField(max_length=500),
        ),
        migrations.AlterField(
            model_name='dev',
            name='dev_name',
            field=models.CharField(max_length=500),
        ),
        migrations.AlterField(
            model_name='extra_info',
            name='rating',
            field=models.CharField(max_length=500),
        ),
        migrations.AlterField(
            model_name='extra_info',
            name='source',
            field=models.CharField(max_length=500),
        ),
        migrations.AlterField(
            model_name='game_info',
            name='game_name',
            field=models.CharField(max_length=500),
        ),
        migrations.AlterField(
            model_name='genre',
            name='genre_name',
            field=models.CharField(max_length=500),
        ),
        migrations.AlterField(
            model_name='publisher',
            name='publisher_name',
            field=models.CharField(max_length=500),
        ),
        migrations.CreateModel(
            name='Theme',
            fields=[
                ('theme_id', models.IntegerField(primary_key=True, serialize=False)),
                ('theme_name', models.CharField(max_length=500)),
                ('game_infos', models.ManyToManyField(to='gameinfo.game_info')),
            ],
        ),
    ]
