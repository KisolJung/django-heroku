from django.db import transaction
from django.http import Http404
from django.contrib.auth.models import User
from django.utils.decorators import method_decorator
from ..decorators import auth_required
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from ..serializers import UserProfileSerializer, BoardSerializer


class MentorView(APIView):
    @transaction.atomic
    @method_decorator(auth_required)
    def post(self, request):
        serializer = BoardSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

"""
class UserView(APIView):
    serializer_class = UserProfileSerializer

    @method_decorator(auth_required)
    def get(self, request):
        serializer = self.serializer_class(request.user)
        return Response(serializer.data)
"""
