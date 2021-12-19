from django.db import transaction
from django.http import Http404
from django.utils.decorators import method_decorator
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from ..models import Board, Match
import datetime


def get_board(board_id):
    try:
        board = Board.objects.get(id=board_id, is_deleted=False)
        if not board.is_finished:
            if board.finish_dt <= datetime.datetime.now():
                board.is_finished = True
                board.save()
        return board
    except Board.DoesNotExist:
        raise Http404

class MenteeView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def check_match(self, mentee_id, board_id):
        try:
            match = Match.objects.get(mentee_id=mentee_id, board_id=board_id)
        except Match.DoesNotExist:
            return True
        else:
            return True if match is None else False

    def mentee_nums(self, board_id):
        try:
            match_list = Match.objects.filter(board_id=board_id)
        except Match.DoesNotExist:
            return 0
        else:
            return len(match_list)

    @transaction.atomic
    def get(self, request, board_id):
        board = get_board(board_id)
        if board.is_closed or board.is_finished:
            return Response({"message": "이미 마감된 멘토링 입니다."}, status=status.HTTP_400_BAD_REQUEST)
        elif self.mentee_nums(board_id) >= board.mentee_nums:
            return Response({"message": "이미 멘티가 모두 모집된 멘토링입니다."}, status=status.HTTP_400_BAD_REQUEST)

        if board.mentor.id == request.user.id:
            return Response({"message": "자신의 멘토링은 신청할 수 없습니다."}, status=status.HTTP_400_BAD_REQUEST)
        if self.check_match(request.user.id, board.id):
            match = Match(mentee=request.user, board=board)
            match.save()
            return Response({"message": "멘토링 신청이 완료되었습니다."}, status=status.HTTP_201_CREATED)
        res = {"message": "이미 신청한 멘토링 입니다."}
        return Response(res, status=status.HTTP_400_BAD_REQUEST)

    @transaction.atomic
    def post(self, request, board_id):
        board = get_board(board_id)
        if self.check_match(request.user.id, board.id):
            return Response({"message": "신청하지 않은 멘토링은 평가할 수 없습니다."}, status=status.HTTP_400_BAD_REQUEST)
        match = Match.objects.get(mentee_id=request.user.id, board_id=board_id)
        if match.is_rated:
            return Response({"message": "이미 평가한 멘토링 입니다."}, status=status.HTTP_400_BAD_REQUEST)

        up_down = int(request.data.get("up_down"))
        match.up_down = up_down
        match.is_rated = True
        match.save()

        profile = board.mentor.profile
        profile.temperature = profile.temperature + up_down
        profile.save()
        return Response({"message": "평가가 완료되었습니다."}, status=status.HTTP_200_OK)
