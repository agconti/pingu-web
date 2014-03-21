from rest_framework import serializers
from core.models import Match, Score, Ranking
from users.models import User


class MatchSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Match


class UserSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = User


class ScoreSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Score


class RankingSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Ranking
