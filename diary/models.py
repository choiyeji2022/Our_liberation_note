from django.db import models
from django.urls import reverse

from user.models import Group, User


# 예지
class Note(models.Model):
    pass


# 미영
class PlanPage(models.Model):
    note = models.ForeignKey("Note", on_delete=models.CASCADE)
    category = models.CharField(max_length=100)
    date = models.DateField(auto_now_add=True)
    place = models.CharField(max_length=100)
    location = models.CharField(max_length=255)
    time = models.CharField(max_length=255)
    memo = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)


# 제건
class PhotoPage(models.Model):
    pass


class Photo(models.Model):
    pass


class Comment(models.Model):
    pass


# 예린
class Stamp(models.Model):
    pass


class Todo(models.Model):
    pass
