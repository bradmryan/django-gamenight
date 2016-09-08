import requests

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

from .models import Game, Player
from . import config

# Create your views here.
def get_games_for_user(steam_key, steam_id):
    '''
    Get list of games owned by player
    '''
    game_list = []
    response = requests.get("http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key=" + steam_key + "&steamid=" + steam_id + "&format=json").json()
    for obj in response.get("response").get("games"):
        game_list.append(obj.get("appid"))
        game_list.sort()
    return game_list


def get_game_name_by_id_2(steam_key, app_id):
    '''
    Method 2 for getting Steam game data.
    Requires a Steam dev key.
    Returns the game name is successful.
    Returns No App Data if fail.
    '''
    response = requests.get("http://api.steampowered.com/ISteamUserStats/GetSchemaForGame/v2/?key=" + steam_key + "&appid=" + str(app_id)).json()
    if response.get("game"):
        return response.get("game").get("gameName")
    else:
        return "No App Data"

def get_game_name_by_id(app_id, steam_key):
    '''
    Method 1 for getting Steam game data.
    Does not require a Steam dev key to perform.
    Returns game name if successful.
    Returns function if fail.
    '''
    response = requests.get("http://store.steampowered.com/api/appdetails?appids=" + str(app_id)).json()
    if response.get(str(app_id)).get("data"):
        return response.get(str(app_id)).get("data").get("name")
    else:
        return get_game_name_by_id_2(steam_key, app_id)

def get_unique_list(*args):
    super_list = []
    for lst in args:
        for games in lst:
            for game in games:
                if game not in super_list:
                    super_list.append(game)

    return super_list


def home(request):
    STEAM_KEY = config.STEAM_KEY
    MINIMUM_MATCHES = config.MINIMUM_MATCHES

    context = {}
    all_games = []
    game_list_list = []
    match_list = []
    number_of_players = 0

    players = Player.objects.all()

    number_of_players = players.count()

    context["players"] = []

    for player in players:
        game_list = get_games_for_user(STEAM_KEY, player.steam_id)
        context["players"].append({ "name": player.name, "list": game_list  })
        game_list_list.append(game_list)

    list_of_all = get_unique_list(game_list_list)
    list_of_all.sort()


    for app_id in list_of_all:
        matches = 0
        match = {}

        for player in context["players"]:
            if app_id in player["list"]:
                matches += 1

        if matches >= MINIMUM_MATCHES:
            if Game.objects.filter(app_id=app_id).exists():
                game = Game.objects.get(app_id=app_id)
                game_name = game.game_name
            else:
                game_name = get_game_name_by_id(app_id, STEAM_KEY)
                new_game = Game(app_id=app_id, game_name=str(game_name))
                try:
                    new_game.save()
                except:
                    pass
            match = { "appId": app_id, "matches": matches, "gameName": game_name}
            match_list.append(match)

    context["all"] = list_of_all
    context["matches"] = match_list
    context["number_of_players"] = number_of_players
    context["minimum_matches"] = MINIMUM_MATCHES
    context["title"] = config.TITLE
    context["banner_image"] = config.BANNER_IMAGE

    return render(request, 'gamenight/home.html', context)
