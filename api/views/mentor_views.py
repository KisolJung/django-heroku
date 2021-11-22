from django.db import transaction
from django.http import Http404
from django.contrib.auth.models import User
from django.utils.decorators import method_decorator
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from ..decorators import auth_required
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from ..serializers import BoardCreateSerializer, BoardSerializer
from ..models import Board


class MentorView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def post(self, request):
        serializer = BoardCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(request=request)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @method_decorator(auth_required)
    def get(self, request):
        query = Board.objects.all()
        serializer = BoardSerializer(query)
        return Response(serializer.data)


