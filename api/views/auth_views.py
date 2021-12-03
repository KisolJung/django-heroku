from django.db import transaction
from django.http import Http404
from django.contrib.auth.models import User
from django.utils.decorators import method_decorator
from ..decorators import auth_required
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from ..serializers import LoginSerializer, RegisterSerializer, UserProfileSerializer


class SignupView(APIView):
    @transaction.atomic
    def post(self, request):
        register_serializer = RegisterSerializer(data=request.data)
        if register_serializer.is_valid():
            register_serializer.save(request=request)
            return Response(status=status.HTTP_201_CREATED)
        return Response(register_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    @transaction.atomic
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        token, created = Token.objects.get_or_create(user=user)
        return Response({'Token': token.key})


class UserDetailView(APIView):
    serializer_class = UserProfileSerializer

    def get_object(self, id):
        try:
            user = User.objects.get(pk=id)
            return user
        except User.DoesNotExist:
            raise Http404

    def get(self, request, id):
        query = self.get_object(id)
        serializer = self.serializer_class(query)
        return Response(serializer.data)


class UserDuplicateView(APIView):
    serializer_class = UserProfileSerializer

    def get_object(self, username):
        try:
            return User.objects.get(username=username)
        except User.DoesNotExist:
            return None

    def get(self, request, username):
        res = {"is_exist": False}
        user = self.get_object(username)
        if user is not None:
            res["is_exist"] = True
        return Response(res, status=status.HTTP_200_OK)


class UserView(APIView):
    serializer_class = UserProfileSerializer

    @method_decorator(auth_required)
    def get(self, request):
        serializer = self.serializer_class(request.user)
        return Response(serializer.data)


class UserSwitchViews(APIView):
    serializer_class = UserProfileSerializer

    def get_object(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

    @method_decorator(auth_required)
    def get(self, request):

        user = self.get_object(request.user.id)
        login_as = user.profile.login_as

        user.profile.login_as = False if login_as else True

        user.profile.save()

        serializer = self.serializer_class(request.user)
        return Response(serializer.data)

