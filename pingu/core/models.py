from model_utils.models import TimeStampedModel
from django.db import models
from users.models import User
from config import settings

# Create your models here.


class Match(TimeStampedModel):
    winner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="winner")
    loser = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="loser")
