from core.models import Match, Ranking
from users.models import User
from api.serializers import (MatchSerializer, UserSerializer, RankingSerializer,
    CreateUserSerializer, PasswordSerializer)
from django.db import IntegrityError
from rest_framework.response import Response
from rest_framework import mixins, generics, status, viewsets
from rest_framework.authentication import TokenAuthentication, BasicAuthentication, SessionAuthentication
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from .authentication import UnsafeSessionAuthentication
from .permissions import IsSelf


class MatchViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """
    queryset = Match.objects.all()
    serializer_class = MatchSerializer
    authentication_classes = (TokenAuthentication, SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)


class MatchResultsView(APIView):
    """
    Create the match and score records from a fierce ping pong match.
    """
    queryset = Ranking.objects.all()
    serializer_class = MatchSerializer
    authentication_classes = (TokenAuthentication, SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        serializer = MatchSerializer(data=request.DATA)
        if serializer.is_valid():
            try:

                user_ranking = Ranking.objects.get(player=request.user)
                user_ranking.save(match=serializer.object)
                user_ranking = RankingSerializer(user_ranking)
                return Response(user_ranking.data, status=status.HTTP_201_CREATED)
            except IntegrityError:
                return Response({"msg": "User does not exist."}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserList(mixins.CreateModelMixin, generics.GenericAPIView):
    """
    This view generates a list of users and upon posting.
    """
    queryset = User.objects.all()
    authentication_classes = (UnsafeSessionAuthentication,)
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = CreateUserSerializer(data=request.DATA)
        if serializer.is_valid():
            try:
                created_user = User.objects.create_user(**serializer.data)
                returned_user = UserSerializer(created_user)
                return Response(returned_user.data, status=status.HTTP_201_CREATED)
            except IntegrityError:
                return Response({"msg": "User already exists."}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserDetail(mixins.RetrieveModelMixin, generics.GenericAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = (TokenAuthentication, SessionAuthentication)
    permission_classes = (IsSelf,)

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


class UserLogin(APIView):
    queryset = User.objects.all()
    authentication_classes = (BasicAuthentication, TokenAuthentication)
    permission_classes = (IsAuthenticated,)

    def post(self, request, format=None):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)


class ChangePasswordView(APIView):
    '''
    Changes a user's password
    '''
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = (TokenAuthentication, SessionAuthentication)
    permission_classes = (IsSelf,)

    def post(self, request, *args, **kwargs):
        user = request.user
        serializer = PasswordSerializer(data=request.DATA)
        if not serializer.data['new_password'] == serializer.data['confirmation_password']:
            return Response({"msg": "password and confirmation password dont match."},
                            status=status.HTTP_400_BAD_REQUEST)
        if serializer.is_valid():
            user.set_password(serializer.data['new_password'])
            user.save()
            return Response({'msg': 'password set'}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RankingViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """
    queryset = Ranking.objects.all()
    serializer_class = RankingSerializer
    authentication_classes = (TokenAuthentication, SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)
