from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    point = models.IntegerField(default=0)
    school = models.CharField(max_length=150, blank=True)
    student_number = models.CharField(max_length=150, blank=True)
    major = models.CharField(max_length=150, blank=True)
    # login_as = models.BooleanField(default=False)
    temperature = models.IntegerField(default=36)
    thumbnail = models.ImageField(upload_to='thumbnail/%Y/%m/%d/', blank=True, null=True)


class Board(models.Model):
    id = models.BigAutoField(primary_key=True)
    mentor = models.ForeignKey(User, on_delete=models.CASCADE)

    title = models.CharField(max_length=200, blank=True)
    contents = models.TextField(blank=True)
    mentee_nums = models.IntegerField(default=1)
    term = models.IntegerField(default=1)
    link = models.TextField(blank=True)

    is_closed = models.BooleanField(default=False) # 모집 마감
    finish_dt = models.DateTimeField(null=True)  # 종료일
    is_finished = models.BooleanField(default=False) # 멘토링 종료

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)


class Match(models.Model):
    id = models.BigAutoField(primary_key=True)
    mentee = models.ForeignKey(User, on_delete=models.CASCADE)
    board = models.ForeignKey(Board, on_delete=models.CASCADE)
    up_down = models.IntegerField(default=0)
    is_rated = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

