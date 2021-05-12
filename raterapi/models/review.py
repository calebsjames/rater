from django.db import models


class Review(models.Model):

    game_id = models.ForeignKey("Game", on_delete=models.CASCADE)
    rating = models.IntegerField()
    text = models.CharField(max_length=250)
    user_id = models.ForeignKey("Gamer", on_delete=models.CASCADE)

    