from model_utils.models import TimeStampedModel
from django.db import models
from config import settings


class Match(TimeStampedModel):
    winner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="winner")
    loser = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="loser")


class Score(TimeStampedModel):
    match = models.ForeignKey(Match, related_name="match")
    player = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="player")
    score = models.IntegerField()
