from model_utils.models import TimeStampedModel
from django.db import models
from config import settings
import math


class Match(TimeStampedModel):
    winner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="won_matches")
    loser = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="lost_matches")
    winner_score = models.IntegerField()
    loser_score = models.IntegerField()


class Ranking(TimeStampedModel):
    player = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="rank")
    elo_rating = models.FloatField(default=1400)
    best_score_differential = models.FloatField(default=0)
    worst_score_differential = models.FloatField(default=0)
    heighest_ranking = models.FloatField(default=0)

    def save(self, match=None, *args, **kwargs):
        '''
        Updates a user's ranking with a match.
        '''
        if match is None:
            return super(Ranking, self).save(*args, **kwargs)
        self.calculate_elo_rating(match)
        if match.winner == self.player:
            self.calculate_best_score_differential(match)
        else:
            self.calculate_worst_score_differential(match)
        self.calculate_heighest_ranking()
        super(Ranking, self).save(*args, **kwargs)

    def calculate_elo_rating(self, match):
        '''
        Caclulates the elo score for a user
        '''
        win_value = 1
        loss_value = 0
        kfactor = 32
        if match.winner == self.player:
            rank_difference = self.elo_rating - match.loser.rank.model().elo_rating
        else:
            rank_difference = self.elo_rating - match.winner.rank.model().elo_rating
        win_chance = 1 / (1 + (math.pow(10, (rank_difference / 400))))
        self.elo_rating = self.elo_rating + kfactor * (win_value - win_chance)

    def calculate_best_score_differential(self, match):
        """
        Needs to be refactored to differential
        """
        winner_score = match.score.winner
        looser_score = match.score.loser
        differential = (winner_score - looser_score) / winner_score
        if self.best_score > differential:
            self.best_score = differential

    def calculate_worst_score_differential(self, match):
        """
        Needs to be refactored to differential
        """
        winner_score = match.score.winner
        looser_score = match.score.loser
        differential = (winner_score - looser_score) / winner_score
        if self.worst_score < differential:
            self.worst_score = differential

    def calculate_heighest_ranking(self):
        if self.heighest_ranking < self.elo_rating:
            self.heighest_ranking = self.elo_rating
