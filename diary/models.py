from django.db import models
from django.urls import reverse
from user.models import Group, User


#status 종류
status_choice = (
        ('0', '활성화'),
        ('1', '비활성화'),
        ('2', '강제중지'),
        ('3', '삭제'),
    )


# 예지
class Note(models.Model):
    pass


# 미영
class PlanPage(models.Model):
    note = models.ForeignKey("Note", on_delete=models.CASCADE)
    category = models.CharField(max_length=100)
    start = models.DateField()
    title = models.CharField(max_length=100)
    location = models.CharField(max_length=255)
    time = models.CharField(max_length=255)
    memo = models.CharField(max_length=100)
    status = models.CharField(choices=status_choice, max_length=100)


# 제건
class PhotoPage(models.Model):
    photo_diary = models.IntegerField()
    category = models.CharField(max_length=100)
    image = models.ImageField()
    location = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    memo = models.CharField(null= True, max_length=100)
    status = models.CharField(max_length=100)
    

    def __str__(self):
        return self.name


class Comment(models.Model):
    photo = models.ForeignKey(PhotoPage, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.CharField(max_length=256)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name


# 예린
class Stamp(models.Model):
    pass


class Todo(models.Model):
    pass
