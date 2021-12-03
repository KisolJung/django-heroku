from django.db import transaction
from django.http import Http404
from django.contrib.auth.models import User
from django.utils.decorators import method_decorator
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from ..decorators import auth_required,  is_mentor
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .base_views import check_user
from ..serializers import BoardCreateSerializer, BoardSerializer, BoardPutSerializer
from ..models import Board


def check_board_deleted(board_id):
    try:
        board = Board.objects.get(pk=board_id)
    except Board.DoesNotExist:
        raise Http404
    else:
        if board.is_deleted:
            message = {"message": "이미 삭제된 멘토링입니다."}
            return Response(message, status=status.HTTP_403_FORBIDDEN)


class MentorView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @transaction.atomic
    @method_decorator(is_mentor)
    def post(self, request):
        serializer = BoardCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(request=request)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        query = Board.objects.all().filter(is_deleted=False)
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
        check_board_deleted(board_id)
        serializer = BoardSerializer(query)
        return Response(serializer.data)

    @method_decorator(is_mentor)
    def put(self, request, board_id):
        board = self.get_object(board_id)

        if board.is_deleted:
            message = {"message": "이미 삭제된 멘토링입니다."}
            return Response(message, status=status.HTTP_403_FORBIDDEN)

        if not check_user(board.mentor.id, request.user.id):
            message = {"message": "작성자가 아닙니다."}
            return Response(message, status=status.HTTP_403_FORBIDDEN)
        serializer = BoardPutSerializer(board, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @method_decorator(is_mentor)
    def patch(self, request, board_id):
        board = self.get_object(board_id)
        if board.is_deleted:
            message = {"message": "이미 삭제된 멘토링입니다."}
            return Response(message, status=status.HTTP_403_FORBIDDEN)

        if not check_user(board.mentor.id, request.user.id):
            message = {"message": "작성자가 아닙니다."}
            return Response(message, status=status.HTTP_403_FORBIDDEN)
        if board.is_closed:
            message = {"message": "이미 마감된 멘토링입니다."}
            return Response(message, status=status.HTTP_403_FORBIDDEN)
        board.is_closed = True
        board.save()
        message = {"message": "조기 마감 처리 했습니다."}
        return Response(message, status=status.HTTP_200_OK)
        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @method_decorator(is_mentor)
    def delete(self, request, board_id):
        board = self.get_object(board_id)
        if not check_user(board.mentor.id, request.user.id):
            message = {"message": "작성자가 아닙니다."}
            return Response(message, status=status.HTTP_403_FORBIDDEN)
        if board.is_closed:
            message = {"message": "이미 삭제된 멘토링입니다."}
            return Response(message, status=status.HTTP_403_FORBIDDEN)
        board.is_deleted = True
        board.save()
        message = {"message": "삭제 완료되었습니다."}
        return Response(message, status=status.HTTP_200_OK)



