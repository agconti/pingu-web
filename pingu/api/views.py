from django.shortcuts import render
from core.models import Match
from users.models import User
from api.serializers import MatchSerializer
from rest_framework import viewsets

# Create your views here.

class MatchViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """
    queryset = Match.objects.all()
    serializer_class = MatchSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
