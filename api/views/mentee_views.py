from django.db import transaction
from django.http import Http404
from django.utils.decorators import method_decorator
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from ..models import Board, Match


class MenteeView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_board(self, board_id):
        try:
            return Board.objects.get(pk=board_id)
        except Board.DoesNotExist:
            raise Http404

    def check_match(self, mentee_id, board_id):
        try:
            match = Match.objects.get(mentee_id=mentee_id, board_id=board_id)
        except Match.DoesNotExist:
            return True
        else:
            return True if match is None else False

    @transaction.atomic
    def get(self, request, board_id):
        board = self.get_board(board_id)
        if board.mentor.id == request.user.id:
            return Response({"message": "자신의 멘토링은 신청할 수 없습니다."}, status=status.HTTP_400_BAD_REQUEST)
        if self.check_match(request.user.id, board.id):
            match = Match(mentee=request.user, board=board)
            match.save()
            return Response({"message": "멘토링 신청이 완료되었습니다."}, status=status.HTTP_201_CREATED)
        res = {"message": "이미 신청한 멘토링 입니다."}
        return Response(res, status=status.HTTP_400_BAD_REQUEST)

