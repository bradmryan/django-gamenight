from django.contrib import admin
from .models import Game, Player
# Register your models here.
REGISTER_MODELS = [
    Game,
    Player
]

admin.site.register(REGISTER_MODELS)
