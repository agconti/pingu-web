from rest_framework import serializers
from core.models import Match, Score, Ranking
from users.models import User


class MatchSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Match


class ScoreSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Score


class RankingSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Ranking


class UserSerializer(serializers.HyperlinkedModelSerializer):
    match = MatchSerializer(many=True, read_only=True)
    ranking = RankingSerializer(many=True, read_only=True)
    auth_token = serializers.SlugRelatedField(read_only=True, slug_field='key')

    class Meta:
        model = User
        fields = ('url', 'first_name', 'last_name',
                  'username', 'auth_token')
