from django.db import models

# Create your models here.
class Game(models.Model):
    app_id = models.CharField(max_length=50, unique=True)
    game_name = models.CharField(max_length=255)

    def __str__(self):
        return self.game_name + " " + self.app_id


class Player(models.Model):
    name = models.CharField(max_length=255)
    steam_id = models.CharField(max_length=255)

    def __str__(self):
        return self.name
