from django.db import models
from igdb.wrapper import IGDBWrapper
from datetime import datetime, date, timedelta
from django.db.models import Q, Max
import json
import environ

CATERGORY_ENUM = {
    0: "Main game",
    1: "DLC",
    2: "Expansion",
    4: "Standalone expansion",
    8: "Remake",
    9: "Remaster",
    10: "Expanded game",
    11: "port"
}
#Uses env to store the api access information
env = environ.Env()
environ.Env.read_env()
wrapper = IGDBWrapper(env('CLIENT_ID'), env("ACCESS_TOKEN")) 


            
class Console(models.Model):
    console_id = models.IntegerField(primary_key=True)
    console_name = models.CharField(max_length=500)
    objects = models.Manager()

    def __str__(self):
        return self.console_name

class seasonapiManager(models.Manager):
    def get_seasonal_games(self, season, year, order):
        """
        Takes a season, year, and a sort order and uses that to query the database for games belonging to all of them
        returns a query of those parameters
        """
        return (Game_info.objects.annotate(max_sort=Max(order))
                .filter(Q(release_time__season=season) & Q(release_time__date__contains=year))
                .order_by('max_sort'))
    
    def get_limited_games(self, season, year, limit, item, order):
        """
        Same as seasonal games but takes a additional limit parameter to limit the items
        returns a query with the parameters
        """
        if limit == 'console':
            return (Game_info.objects.annotate(max_sort=Max(order))
                    .filter(Q(release_time__season=season) & Q(release_time__date__contains=year)
                    & Q(consoles__console_name=item)).order_by('max_sort'))
        
        elif limit == 'theme':
            return (Game_info.objects.annotate(max_sort=Max(order))
                    .filter(Q(release_time__season=season) & Q(release_time__date__contains=year)
                    & Q(theme__theme_name=item)).order_by('sortby'))

        elif limit == 'genre':
            return (Game_info.objects.annotate(max_sort=Max(order))
                    .filter(Q(release_time__season=season) & Q(release_time__date__contains=year) 
                    & Q(genre__genre_name=item)).order_by('max_sort'))
        
    def get_just_released_games(self):
        """
        takes no parameters and returns games released within the last 30 days using time delta to calculated it
        return the queryset
        """
        today = date.today()
        past = today - timedelta(days=30)
        return (Game_info.objects.annotate(max_sort=Max('release_time__date'))
                    .filter(Q(release_time__date__gte=past) & Q(release_time__date__lte=today)).order_by('-max_sort'))
    
    def get_TBA_games(self):
        """
        takes no parameters and returns games with no scheduled release date
        return the queryset
        """
        return (Game_info.objects.annotate(max_sort=Max('hype__average_hype'))
                    .filter(Q(release_time__season ='TBA' )).order_by('max_sort'))


class Game_info(models.Model):
    game_id = models.IntegerField(primary_key=True)
    game_name= models.CharField(max_length=500)
    consoles = models.ManyToManyField(Console)
    objects = models.Manager()
    seasonalobjects = seasonapiManager()
     
    def __str__(self):
        return self.game_name
    class Meta:
        ordering = ['game_name']

class Hype(models.Model):
    game_id = models.ForeignKey(Game_info, on_delete=models.CASCADE)
    is_hype = models.IntegerField(default=0)
    maybe_hype = models.IntegerField(default=0)
    not_hype = models.IntegerField(default=0)
    average_hype = models.IntegerField(default=0)

    def get_average_hype(self):
        if self.is_hype or self.maybe_hype:
            self.average_hype = (((self.is_hype * 100) + (self.maybe_hype * 50))
            / (self.is_hype + self.maybe_hype + self.not_hype))

class Dev(models.Model):
    dev_id = models.IntegerField(primary_key=True)
    dev_name = models.CharField(max_length=500)
    game_infos = models.ManyToManyField(Game_info)

    def __str__(self):
        return self.dev_name
    
class Publisher(models.Model):
    publisher_id = models.IntegerField(primary_key=True)
    publisher_name = models.CharField(max_length=500)
    game_infos = models.ManyToManyField(Game_info)

    def __str__(self):
        return self.publisher_name

class genreManager(models.Manager):
    def pull_genres(self, genre):
        return Genre.objects.get(genre_name=genre).game_info_set.all()
    
class Genre(models.Model):
    genre_id = models.IntegerField(primary_key=True)
    genre_name = models.CharField(max_length=500)
    game_infos = models.ManyToManyField(Game_info)
    objects = models.Manager()
    genreobjects = genreManager()

    def __str__(self):
        return self.genre_name

class themeManager(models.Manager):
    def pull_themes(self, theme):
        return Theme.objects.get(theme_name=theme).game_info_set.all()
    
class Theme(models.Model):
    theme_id = models.IntegerField(primary_key=True)
    theme_name = models.CharField(max_length=500)
    game_infos = models.ManyToManyField(Game_info)
    objects = models.Manager()
    themeobjects = themeManager()

    def __str__(self):
        return self.theme_name

class Extra_info(models.Model):
    game_id = models.ForeignKey(Game_info, on_delete=models.CASCADE)
    description = models.CharField(max_length=10000)
    source = models.CharField(max_length=500)


class Release_time(models.Model):
    game_id = models.ForeignKey(Game_info, on_delete=models.CASCADE)
    date = models.DateField(default=date.today, blank=True, null=True)
    season = models.CharField(max_length=30)

class Artwork(models.Model):
    artwork_id = models.IntegerField(primary_key=True)
    image = models.ImageField(blank=True, null=True)
    game_infos = models.ManyToManyField(Game_info)

class Screenshot(models.Model):
    screenshot_id = models.IntegerField(primary_key=True)
    image = models.ImageField(blank=True, null=True)
    game_infos = models.ManyToManyField(Game_info)
        
async def populate_database(begin, end):
    """
    Takes a beginning unix timestamp and a ending unix timestamp and makes a api call to make modesl for
    database with the response
    """
    byte_array = wrapper.api_request(
            'games',
            f'''
            fields id, name, platforms.name, involved_companies.developer, genres , genres.name,screenshots,
            summary, category, storyline, category, themes.name, first_release_date, artworks, artworks.url,screenshots.url,
            involved_companies.publisher, involved_companies.company.name, age_ratings.category, age_ratings.rating;
            where category = (0,1,2,4,8,9,10,11) & first_release_date >= {begin} & first_release_date <= {end};
            sort id asc;
            limit 500;
            '''
          )
    data = json.loads(str(byte_array, 'utf-8'))
    for item in data:
        game = Game_info(game_id=item['id'], game_name=item["name"])
        game.save()
        if 'platforms' in item:
            for devices in item['platforms']:
                platform = Console(console_id=devices["id"], console_name=devices['name'])
                platform.save()
                game.consoles.add(platform)
        if "involved_companies" in item:
            for companies in item["involved_companies"]:
                if companies['developer']:
                    developer = Dev(dev_id=companies['company']['id'], dev_name=companies['company']['name'])
                    developer.save()
                    developer.game_infos.add(game)
                if companies['publisher']:
                    publisher = Publisher(publisher_id=companies['company']['id'], publisher_name=companies['company']['name'])
                    publisher.save()
                    publisher.game_infos.add(game)
        if 'themes' in item:
            for themes in item["themes"]:
                theme = Theme(theme_id=themes["id"], theme_name=themes["name"])
                theme.save()
                theme.game_infos.add(game)
        if "genres" in item:
            for genres in item["genres"]:
                genre = Genre(genre_id=genres["id"], genre_name=genres["name"])
                genre.save()
                genre.game_infos.add(game)
        if 'artworks' in item:
            for art in item['artworks']:
                artitem = Artwork(artwork_id=art['id'], image=art['url'])
                artitem.save()
                artitem.game_infos.add(game)
        if 'screenshots' in item:
            for screenshot in item['screenshots']:
                screenitem = Screenshot(screenshot_id=screenshot['id'], image=screenshot['url'])
                screenitem.save()
                screenitem.game_infos.add(game)
        firstdate = None
        month = ''
        if 'first_release_date' in item:
            first_release_date = item['first_release_date']
            firstdate = datetime.fromtimestamp(first_release_date).date()
            month = firstdate.month
        game_season = ''
        if month in [12, 1, 2]:
            game_season = 'Winter'
        elif month in [3, 4, 5]:
            game_season = 'Spring'
        elif month in [6, 7, 8]:
            game_season = 'Summer'
        elif month in [9, 10, 11]:
            game_season = 'Fall'
        else:
            game_season = 'TBA'
        release = Release_time(game_id=game,date=firstdate, season=game_season)
        release.save()
        release.game_id = game
        hype = Hype(game_id=game)
        hype.save()
        hype.game_id = game
        game_type = "TBA"
        if 'category' in item:
            game_type = CATERGORY_ENUM[item['category']]
        story = "TBA"
        if "storyline" in item:
            if len(item["storyline"]) <= 10000:
                story = item["storyline"]
        extra_info = Extra_info(game_id=game,description=story, source=game_type)
        extra_info.save()
        extra_info.game_id = game
def get_timestamp(season, year):
    """
    Passes a season and year and returns an array with 2
    timestamp so you can pass to the api call to narrow the results
    """
    currentstart = 0
    currentend = 0
    if season == "Winter":
        today = date.today()
        currentmonth = today.month
        if currentmonth == 12:
            currentstart = datetime(int(year),12,1)
            currentend = datetime(int(year) + 1,3,1)
        else:
            currentstart = datetime(int(year)-1,12,1)
            currentend = datetime(int(year) + 1,3,1)
    elif season == "Spring":
        currentstart = datetime(int(year),3,1)
        currentend = datetime(int(year) +1,6,1)
    elif season == "Fall":
        currentstart = datetime(int(year),6,1)
        currentend = datetime(int(year),9,1)
    else:
        currentstart = datetime(int(year),9,1)
        currentend = datetime(int(year),11,1)
    return [datetime.timestamp(currentstart), datetime.timestamp(currentend)]