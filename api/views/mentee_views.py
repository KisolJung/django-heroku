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
from ..serializers import MatchCreateSerializer
from ..models import Board, Match


class MenteeView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_board(self, board_id):
        try:
            return Board.objects.get(pk=board_id)
        except Board.DoesNotExist:
            raise Http404

    def get(self, request, board_id):
        data = request.data
        data['board'] = self.get_board(board_id)
        data['mentee'] = request.user
        serializer = MatchCreateSerializer(data)
        return Response(serializer.data)




