from rest_framework import serializers
from gameinfo.models import *

class HypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hype
        exclude = ['id','game_id']

class DevSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dev
        fields = ('dev_name',)

class PublisherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Publisher
        fields = ('publisher_name',)
class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        exclude = ['genre_id', 'game_infos']

class ThemeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Theme
        exclude = ['theme_id', 'game_infos']

class Extra_InfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Extra_info
        exclude=['id', 'game_id']

class Release_TimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Release_time
        exclude = ['id', 'game_id']

class ArtworkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artwork
        exclude = ['artwork_id', 'game_infos']

class ScreenshotSerializer(serializers.ModelSerializer):
    class Meta:
        model = Screenshot
        exclude = ['screenshot_id', 'game_infos']

class ConsoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Console
        fields = ('console_name',)

class Game_InfoSerializer(serializers.ModelSerializer):
    consoles = ConsoleSerializer(read_only=True, many=True)
    developer = DevSerializer(read_only=True, many=True, source='dev_set')
    publisher = PublisherSerializer(read_only=True, many=True, source='publisher_set')
    artwork = ArtworkSerializer(read_only=True, many=True, source="artwork_set")
    screenshot = ScreenshotSerializer(read_only=True, many=True, source="screenshot_set")
    genre = GenreSerializer(read_only=True, many=True, source='genre_set')
    theme = ThemeSerializer(read_only=True, many=True, source='theme_set')
    release_date = Release_TimeSerializer(read_only=True, many=True, source='release_time_set')
    hype = HypeSerializer(read_only=True, many=True, source="hype_set")
    extra_info = Extra_InfoSerializer(read_only=True, many=True, source="extra_info_set")

    class Meta:
        model = Game_info
        fields = (
            'game_id',
            'game_name',
            'consoles',
            'developer',
            'publisher',
            'artwork',
            'screenshot',
            'genre',
            'theme',
            'release_date',
            'hype',
            'extra_info',
        )

        '''def get_queryset(self, season):
            queryset = Dev.objects.filter()'''
    '''def get_consoles(self, instance):
        consoles = instance.consoles.order_by('console_name')
        return ConsoleSerializer(consoles, many=True).data'''




