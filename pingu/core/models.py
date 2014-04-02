from model_utils.models import TimeStampedModel
from django.db import models
from config import settings
import math


class Match(TimeStampedModel):
    winner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="won_matches")
    loser = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="lost_matches")


class Score(TimeStampedModel):
    match = models.ForeignKey(Match, related_name="score")
    player = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="scores")
    match_score = models.IntegerField()


class Ranking(TimeStampedModel):
    player = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="rank")
    elo_rating = models.IntegerField(default=1400)
    best_score = models.IntegerField(default=0)
    worst_score = models.IntegerField(default=0)
    heighest_ranking = models.IntegerField(default=0)


    def save(self, match, *args, **kwargs):
        score = match.score.match_score
        self.elo_rating = self.calculate_elo_rating(match)
        self.best_score = self.calculate_best_score(score)
        self.worst_score = self.calculate_worst_score(score)
        self.heighest_ranking = self.calculate_heighest_ranking(score)
        super(Ranking, self).save(*args, **kwargs)


    @classmethod
    def calculate_elo_rating(self, match):
        win_value = 1
        loss_value = 0
        kfactor = 32
        if match.winner == self.player:
            rank_difference = self.elo_rating - match.loser.rank.elo_rating
        else:
            rank_difference = self.elo_rating - match.winner.rank.elo_rating
        win_chance = 1 / ( 1 + ( math.pow(10,( rank_difference / 400 ))))
        self.elo_rating = self.elo_rating + kfactor*( win_value - win_chance )


    @classmethod
    def calculate_best_score(self, score):
        if self.best_score > score:
            self.best_score = score


    @classmethod
    def calculate_worst_score(self, score):
        if self.worst < score:
            self.worst = score


    @classmethod
    def calculate_heighest_ranking(self):
        if self.heighest_ranking < self.elo_rating:
            self.heighest_ranking = self.elo_rating
