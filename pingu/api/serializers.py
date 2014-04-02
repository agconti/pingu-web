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
    match = MatchSerializer(read_only=True)

    class Meta:
        model = Ranking
        fields = ('player', 'elo_rating', 'best_score', 'worst_score',
                  'heighest_ranking', 'match')


class UserSerializer(serializers.HyperlinkedModelSerializer):
    match = MatchSerializer(many=True, read_only=True)
    ranking = RankingSerializer(many=True, read_only=True)
    auth_token = serializers.SlugRelatedField(read_only=True, slug_field='key')

    class Meta:
        model = User
        fields = ('url', 'first_name', 'last_name', 'match', 'ranking',
                  'username', 'auth_token')
