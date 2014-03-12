from model_utils.models import TimeStampedModel
from django.db import models
from users.models import User

# Create your models here.


class Match(TimeStampedModel):
    winner = models.ForgeinKey(User)
    loser = models.ForgeinKey(User)
