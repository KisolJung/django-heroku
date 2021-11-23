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
from .base_views import check_user
from ..serializers import BoardCreateSerializer, BoardSerializer, BoardPutSerializer
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
        serializer = BoardSerializer(query, many=True)
        return Response(serializer.data)


class MentorDetailView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_object(self, id):
        try:
            return Board.objects.get(pk=id)
        except Board.DoesNotExist:
            raise Http404

    def get(self, request, board_id):
        query = self.get_object(board_id)
        serializer = BoardSerializer(query)
        return Response(serializer.data)

    def put(self, request, board_id):
        board = self.get_object(board_id)
        serializer = BoardPutSerializer(board, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # patch add
    # delete add

