from model_utils.models import TimeStampedModel
from django.db import models
from config import settings

import math


class Match(TimeStampedModel):
    winner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="won_matches")
    loser = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="lost_matches")
    winner_score = models.IntegerField()
    loser_score = models.IntegerField()

    def __unicode__(self):
        return "Match %s vs %s %s-%s" %(self.winner, self.loser, self.winner_score,
                                        self.loser_score)


class Ranking(TimeStampedModel):
    player = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="rank")
    elo_rating = models.FloatField(default=1400)
    best_score_differential = models.FloatField(default=0)
    worst_score_differential = models.FloatField(default=1)
    heighest_ranking = models.FloatField(default=1400)

    class Meta:
        ordering = ['-elo_rating']

    def save(self, match=None, *args, **kwargs):
        '''
        Updates a user's ranking after a given match.
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
            player_elo_rating = match.loser.rank.model().elo_rating
            win_loss_modifer = win_value
        else:
            player_elo_rating = match.winner.rank.model().elo_rating
            win_loss_modifer = loss_value

        rank_difference = self.elo_rating - player_elo_rating
        win_chance = 1 / (1 + (math.pow(10, (rank_difference / 400))))
        self.elo_rating = self.elo_rating + kfactor * (win_loss_modifer - win_chance)

    def calculate_best_score_differential(self, match):
        total_points_scored = match.winner_score + match.loser_score
        differential = 1 - (match.winner_score - match.loser_score) / float(total_points_scored)
        print differential
        if self.best_score_differential < differential:
            self.best_score_differential = differential
            print self.best_score_differential

    def calculate_worst_score_differential(self, match):
        total_points_scored = match.winner_score + match.loser_score
        differential = (match.winner_score - match.loser_score) / float(total_points_scored)
        print differential
        if self.worst_score_differential > differential:
            self.worst_score_differential = differential
            print self.worst_score_differential

    def calculate_heighest_ranking(self):
        if self.heighest_ranking < self.elo_rating:
            self.heighest_ranking = self.elo_rating

    def __unicode__(self):
        return "%s's Ranking " % self.player.username
