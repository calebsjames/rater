from django.db import models


class Picture(models.Model):

    picture_link = models.CharField(max_length=500)
    game_id = models.ForeignKey("Game", on_delete=models.CASCADE)
    