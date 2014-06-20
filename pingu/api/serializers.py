from rest_framework import serializers
from core.models import Match, Ranking
from users.models import User


class RankingSerializer(serializers.HyperlinkedModelSerializer):
    player_username = serializers.Field(source='player.username')

    class Meta:
        model = Ranking
        fields = ("url", "player", "player_username", "elo_rating",
                  "best_score_differential", "worst_score_differential",
                  "heighest_ranking")


class MatchSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Match


class UserSerializer(serializers.HyperlinkedModelSerializer):
    auth_token = serializers.SlugRelatedField(read_only=True,
                                              slug_field='key')
    rank = RankingSerializer(read_only=True)

    class Meta:
        model = User
        fields = ("url", "first_name", "last_name", "username",
                  "rank", "profile_picture", "auth_token")


class CreateUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ("username", "email", "password", "first_name",
                  "last_name", "profile_picture")


class PasswordSerializer(serializers.Serializer):
    password = serializers.CharField()
    confirmation_password = serializers.CharField()
    new_password = serializers.CharField()

    class Meta:
        fields = ("password", "confirmation_password'",
                  "new_password")
