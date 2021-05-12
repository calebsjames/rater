from django.db import models


class Game(models.Model):

    ages = models.CharField(max_length=10)
    description = models.CharField(max_length=200)
    est_time = models.CharField(max_length=200)
    maker = models.CharField(max_length=30)
    number_of_players = models.IntegerField()
    title = models.CharField(max_length=30)
    year = models.IntegerField()