from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from .models import Profile, Board, Match
from django.contrib.auth import authenticate


class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=50, min_length=2, required=True,
                                     validators=[UniqueValidator(queryset=User.objects.all())])
    password1 = serializers.CharField(write_only=True)
    # password2 = serializers.CharField(write_only=True)
    school = serializers.CharField(max_length=150)
    student_number = serializers.CharField(max_length=150)
    major = serializers.CharField(max_length=150)
    thumbnail = serializers.ImageField(use_url=True, allow_null=True, required=False)

    """
    def validate(self, data):
        if data['password1'] != data['password2']:
            raise serializers.ValidationError("The two password fields didn't match.")
        return data
    """

    def get_cleaned_data(self):
        return {
            'username': self.validated_data.get('username', ''),
            'password1': self.validated_data.get('password1', ''),
            'school': self.validated_data.get('school', ''),
            'student_number': self.validated_data.get('student_number', ''),
            'major': self.validated_data.get('major', ''),
        }

    def save(self, request):
        cleaned_data = self.get_cleaned_data()
        user = User.objects.create_user(
            username=cleaned_data['username'],
            password=cleaned_data['password1']
        )

        thumbnail = self.validated_data.get('thumbnail', None)
        profile \
            = Profile(user=user, school=cleaned_data['school'],
                      student_number=cleaned_data['student_number'],
                      major=cleaned_data['major'],
                      thumbnail=thumbnail)

        user.save()
        profile.save()
        token = Token.objects.create(user=user)

        return token


class LoginSerializer(serializers.Serializer):

    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Unable to log in")


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        exclude = ['id', 'user']


class UserProfileSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()

    class Meta:
        model = User
        fields = ('id', 'username', 'profile')


class BoardSerializer(serializers.ModelSerializer):
    mentor = UserProfileSerializer(read_only=True)

    class Meta:
        model = Board
        exclude = ['created_at', 'updated_at', 'is_deleted']


class BoardPutSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = ('title', 'contents', 'mentee_nums', 'term', 'link')


class BoardCreateSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=20)
    contents = serializers.CharField()
    mentee_nums = serializers.IntegerField(default=1)
    term = serializers.IntegerField(default=1)
    link = serializers.CharField(required=False)

    def get_cleaned_data(self):
        return {
            'title': self.validated_data.get('title', ''),
            'contents': self.validated_data.get('contents', ''),
            'mentee_nums': self.validated_data.get('mentee_nums', ''),
            'term': self.validated_data.get('term', ''),
            'link': self.validated_data.get('link', ''),
        }

    def save(self, request):
        cd = self.get_cleaned_data()
        board\
            = Board(mentor=request.user, title=cd['title'], contents=cd['contents'],
                    mentee_nums=cd['mentee_nums'], term=cd['term'], link=cd['link'],
                    finish_dt=None)
        board.save()
        res = Board.objects.latest('id')

        return res


