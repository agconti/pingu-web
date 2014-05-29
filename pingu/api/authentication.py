from django.contrib.auth import authenticate
from rest_framework import exceptions
from rest_framework.authentication import BasicAuthentication, SessionAuthentication


class UnsafeSessionAuthentication(SessionAuthentication):

    def authenticate(self, request):
        http_request = request._request
        user = getattr(http_request, 'user', None)

        if not user or not user.is_active:
            return None

        return (user, None)
