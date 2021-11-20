from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    point = models.IntegerField(default=0)
    school = models.CharField(max_length=150, blank=True)
    student_number = models.CharField(max_length=150, blank=True)
    major = models.CharField(max_length=150, blank=True)
    login_as = models.BooleanField(default=False)
    temperature = models.IntegerField(default=36)
    thumbnail = models.ImageField(upload_to='thumbnail/%Y/%m/%d/', blank=True, null=True)
