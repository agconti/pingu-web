from core.models import Match, Score, Ranking
from users.models import User
from api.serializers import MatchSerializer, UserSerializer, ScoreSerializer, RankingSerializer
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication, BasicAuthentication, SessionAuthentication


class MatchViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """
    queryset = Match.objects.all()
    serializer_class = MatchSerializer
    authentication_classes = (TokenAuthentication, SessionAuthentication, BasicAuthentication)


class UserViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = (TokenAuthentication, SessionAuthentication, BasicAuthentication)



class ScoreViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """
    queryset = Score.objects.all()
    serializer_class = ScoreSerializer
    authentication_classes = (TokenAuthentication, SessionAuthentication, BasicAuthentication)


class RankingViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """
    queryset = Ranking.objects.all()
    serializer_class = RankingSerializer
    authentication_classes = (TokenAuthentication, SessionAuthentication, BasicAuthentication)
