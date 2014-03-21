from rest_framework import serializers
from core.models import Match
from users.models import User


class MatchSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Match


class UserSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = User
