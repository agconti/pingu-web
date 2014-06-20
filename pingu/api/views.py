from core.models import Match, Ranking
from users.models import User
from api.serializers import (MatchSerializer, UserSerializer, RankingSerializer,
    CreateUserSerializer, PasswordSerializer)
from django.db import IntegrityError
from rest_framework import status, mixins, generics, parsers, renderers, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.serializers import AuthTokenSerializer
from .authentication import UnsafeSessionAuthentication
from .permissions import IsSelf
from django.utils.timezone import now



class ObtainAuthTokenView(APIView):
    '''
    Allows a user to Obtain an auth_token after authenticating.
    '''
    throttle_classes = ()
    permission_classes = ()
    parser_classes = (parsers.FormParser, parsers.MultiPartParser, parsers.JSONParser,)
    renderer_classes = (renderers.JSONRenderer,)
    serializer_class = AuthTokenSerializer
    model = Token

    def post(self, request):
        serializer = self.serializer_class(data=request.DATA)
        if serializer.is_valid():
            token, created = Token.objects.get_or_create(user=serializer.object['user'])
            return Response({'auth_token': token.key})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MatchViewSet(viewsets.ModelViewSet):
    '''
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    '''
    queryset = Match.objects.all()
    serializer_class = MatchSerializer
    authentication_classes = (TokenAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,)


class RankingViewSet(viewsets.ModelViewSet):
    '''
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    '''
    queryset = Ranking.objects.all()
    serializer_class = RankingSerializer
    authentication_classes = (TokenAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,)


class MatchResultsView(APIView):
    '''
    Creates a match and updates rankings after a fierce ping pong match.
    '''
    queryset = Ranking.objects.all()
    serializer_class = MatchSerializer
    authentication_classes = (TokenAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        serializer = MatchSerializer(data=request.DATA)
        if serializer.is_valid():
            try:
                match = serializer.object
                for match_user in [match.loser, match.winner]:
                    # Ranking objects are created automatically when users are.
                    # It should never be the case that a user does not have an
                    # asscoiated ranking object.
                    user_ranking = Ranking.objects.get(player=match_user)
                    user_ranking.save(match=match)
                    if match_user == request.user:
                        updated_ranking = RankingSerializer(user_ranking, context={'request': request})
                return Response(updated_ranking.data, status=status.HTTP_200_OK)
            except IntegrityError:
                return Response({"msg": "User does not exist."}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserList(mixins.CreateModelMixin, generics.GenericAPIView):
    '''
    This view generates a list of users and upon posting.
    '''
    queryset = User.objects.all()
    authentication_classes = (UnsafeSessionAuthentication,)
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = CreateUserSerializer(data=request.DATA, files=request.FILES)
        if serializer.is_valid():
            try:
                created_user = User.objects.create_user(**serializer.data)
                created_user.profile_picture.save("%s.png" % now().strftime("%Y%m%d%H%M%S"),
                                                  serializer.object.profile_picture,
                                                  save=True)
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
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        serializer = UserSerializer(request.user, context={'request': request})
        return Response(serializer.data)


class ChangePasswordView(APIView):
    '''
    Changes a user's password
    '''
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = (TokenAuthentication,)
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
