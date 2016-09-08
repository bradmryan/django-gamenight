!["Game Night"](http://i.imgur.com/IxFjdqX.png "Game Night")


### Requirements

- Django == 1.10.1
- requests == 2.11.1
- A Steam Dev Key https://steamcommunity.com/dev
- Steam Profile IDs for Players

### Installation

In your root Django project folder,
```
git clone https://github.com/bradmryan/django-gamenight.git gamenight
```
Note: This is the folder where manage.py is located.


Register the app in `settings.py`:
```
INSTALLED_APPS = [
    ...
    'gamenight'
]
```
Register the gamenight urls in `urls.py`:
```
urlpatterns = [
    ...
    url(r'', include('gamenight.urls'))
]
```
Update `config.py`, to reflect your project name:
```
from <your_app_name>.settings import DEBUG
```
In `developement`, create dev.py in the gamenight folder. Enter your Steam Developers Key:
```
STEAM_KEY = "##########################"
```
In `production`, create an evironmental variable called STEAM_KEY, to store your steam key.

In your `console`, create migrations for gamenight models, then migrate:
```
python manage.py makemigrations gamenight
```
then,
```
python manage.py migrate gamenight
```
Now you can navigate to your Django admin page, and begin to add players. Once two players have been added, games will begin to auto populate.

### Troubleshooting
- Sometimes, the app will fail the `unique constraint` on the app_id column of the game model. I'm not sure why this happens but it only seems to happen once on it's initial run. Just hit refresh in your browser, and all of your problems should magically disappear.
- No data is populating:
  - Be sure that there are atleast 2 players in database
  - Be sure you are adding the numeric Steam ID associated with the player's Steam profile. NOT the alphanumeric Steam ID.
  - Test your Steam Dev Key and Steam Profile ID using a service like Postman, or your browser. I suggest using Postman because it will give you more insight into the issue. `http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key=<steam_dev_key>&steamid=<numeric_steam_profile_id>&format=json`
- Template conflict:
  - gamenight has a `base.html` template in the `gamenight/templates/` folder. This may conflict with an already existing `base.html` template. If so, delete this file. Note that gamenight relies on a `base.html` template that includes a `head` block at the bottom of the `<head>` of the html, a `body` block in the `<body>`, and a `js` block at the bottom of the `<body>`

### Future updates
- Put app behind authentication.
- Allow users to sign up using tokens assigned to players
- Allow users to vote on a perfered game to play
- Allow users ability to make purchasing suggestions
- Allow users to vote on times for group play
- Allow admin ability to create different groups
- Display group info, such as Discord info, group play times
- Distinguish which games are multiplayer/co-op
