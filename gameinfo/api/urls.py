from gameinfo.api.views import (api_season_game_view,
                                api_limited_game_view,
                                api_just_released_game_info_view,
                                api_TBA_game_info_view,
                                api_like_update_view,
                                )
from django.urls import path

app_name = 'game_info'

urlpatterns = [
    path('Likes/<str:game>', api_like_update_view),
    path('TBA', api_TBA_game_info_view),
    path('just_released', api_just_released_game_info_view),
    path('<str:season>/<int:year>', api_season_game_view),
    path('<str:season>/<int:year>/<str:sorted>', api_season_game_view),
    path('<str:season>/<int:year>/limited/<str:limiter>/<str:item>', api_limited_game_view),
    path('<str:season>/<int:year>/limited/<str:limiter>/<str:item>/<str:sorted>', api_limited_game_view)
]