from django.db import models
from django.urls import reverse

from user.models import Group, User

status_choice = (
    ("0", "활성화"),
    ("1", "비활성화"),
    ("2", "강제중지"),
    ("3", "삭제"),
)


# 예지
class Note(models.Model):
    class Meta:
        db_table = "note"

    note_covers = (
        ("1", "코랄핑크표지"),
        ("2", "브라운표지"),
        ("3", "노랑표지"),
        ("4", "초록표지"),
        ("5", "파랑표지"),
        ("6", "보라표지"),
        ("7", "그라데이션-블루퍼플"),
        ("8", "검정표지"),
        ("9", "그레이블루표지"),
        ("10", "그라데이션-블루옐로"),
        ("11", "그라데이션-보라그레이"),
        ("12", "그라데이션-핑크베이지"),
    )

    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    name = models.CharField("노트이름", max_length=30)
    cateogry = models.CharField("노트표지", choices=note_covers, max_length=10, default=1)
    created_at = models.DateTimeField("생성일", auto_now_add=True)
    status = models.CharField("상태", choices=status_choice, max_length=10, default=0)


# 미영
class PlanPage(models.Model):
    pass


class Memo(models.Model):
    pass


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
