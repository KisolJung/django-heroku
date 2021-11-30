from rest_framework.response import Response
from rest_framework import status


def auth_required(function):
    def wrap(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        return function(request, *args, **kwargs)
    return wrap


def is_mentor(function):
    def wrap(request, *args, **kwargs):
        if not request.user.profile.login_as:
            return Response(status=status.HTTP_403_FORBIDDEN)
        return function(request, *args, **kwargs)
    return wrap
