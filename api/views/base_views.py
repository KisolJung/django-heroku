from django.db import transaction
from django.http import Http404
from django.utils.decorators import method_decorator
from ..decorators import auth_required
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


# Create your views here.
class IndexView(APIView):
    def get(self, request):
        contents = {
            "test_message": "Hello World~"
        }
        return Response(contents, status=status.HTTP_200_OK)


def check_user(owner_id, current_user_id):
    if owner_id == current_user_id:
        return True
    return False
