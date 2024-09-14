from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from gameinfo.models import *
from gameinfo.api.serializers import Game_InfoSerializer
from django.http import HttpResponse, JsonResponse
from rest_framework.parsers import JSONParser

SORT_ENUM = {
    'hype': 'hype__average_hype',
    'alphabetical': 'game_name',
    'release_date': 'release_time__date' 
}




@api_view(['GET',])
def api_just_released_game_info_view(request):
    """Takes a get request and returns a query of games released in the last 30 days"""

    try:
        seasonalgames = Game_info.seasonalobjects.get_just_released_games()

    except:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == "GET":
        serializer  = Game_InfoSerializer(seasonalgames, many='True')
        return JsonResponse(serializer.data, safe=False)

@api_view(['GET',])
def api_TBA_game_info_view(request):
    """Takes a get request and returns a query of games without a release date"""

    try:
        seasonalgames = Game_info.seasonalobjects.get_TBA_games()

    except:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == "GET":
        serializer  = Game_InfoSerializer(seasonalgames, many='True')
        return JsonResponse(serializer.data, safe=False)
    
@api_view(['GET',])
def api_season_game_view(request, season, year, sorted = 'hype'):
    """
    Takes a get request and with the season and the year passed as params and use those to get a query
    from the database with all the games from that peried. the objects are default sorted by hype levels unless passed
    some other sorting parameter. when passed a sort parameter passes it through sort_enum to get the correct query
    to sort by
    after the query the api is called async to potentially update database while returning whats already in the database
    returns a json response
    """
    timep = get_timestamp(season, year)
    populate_database(timep[0],timep[1])
    
    try:
        seasonalgames = Game_info.seasonalobjects.get_seasonal_games(season, year, SORT_ENUM[sorted])
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == "GET":
        
        gameserializer = Game_InfoSerializer(seasonalgames, many='True')
        return JsonResponse(gameserializer.data, safe=False)

@api_view(['GET',])
def api_limited_game_view(request, season, year, limiter, item,  sorted = 'hype'):
    """
    does the same thing as api_season_game_view but takes a limiter parameter which limits which items in the query
    which can potentially be console, genre, or theme 
    """
    timep = get_timestamp(season, year)
    populate_database(timep[0],timep[1])
    
    try:
        seasonalgames = Game_info.seasonalobjects.get_limited_games(season, year,  limiter, item, SORT_ENUM[sorted])
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == "GET":
        
        gameserializer = Game_InfoSerializer(seasonalgames, many='True')
        return JsonResponse(gameserializer.data, safe=False)

@api_view(['POST',])
def api_like_update_view(request, game):
    """
    Takes a post request and checks which hype level was passed back and increases the respective one
    After that is processed the hype models function.get_average_hype recalculates and updates it again
    """
    try:
        data = {}
        hype = Hype.objects.get(game_id__game_name=game)
        hype_type = request.data['hype']
        if hype_type == 'is_hype':
            hype.is_hype += 1
        elif hype_type == 'maybe_hype':
            hype.maybe_hype += 1
        elif hype_type == 'not_hype':
            hype.not_hype += 1
        data['success'] = 'You did it'     
        hype.get_average_hype()    
        hype.save()
        return Response(status=status.HTTP_201_CREATED) 
    except:
        
        return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
    