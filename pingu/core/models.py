from model_utils.models import TimeStampedModel
from django.db import models
from config import settings


class Match(TimeStampedModel):
    winner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="winner")
    loser = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="loser")


class Score(TimeStampedModel):
    match = models.ForeignKey(Match, related_name="match")
    player = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="player+")
    score = models.IntegerField()


class Ranking(TimeStampedModel):
    player = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="player")
    best_score = models.IntegerField()
    worst_score = models.IntegerField()
    heighest_ranking = models.IntegerField()

    @property
    def calculate_elo_ranking(self):
        pass

    @property
    def calculate_best_score(self):
        pass

    @property
    def calculate_worst_score(self):
        pass
