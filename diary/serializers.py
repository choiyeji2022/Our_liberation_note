from rest_framework import serializers
from rest_framework.serializers import ValidationError

from user.models import UserGroup
from user.serializers import GroupSerializer

from .models import Comment, Note, PhotoPage, PlanPage, Stamp


# 노트 일반 CRUD
class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = "__all__"


# 노트에 들어 가는 모든 photo, Plan
class DetailNoteSerializer(serializers.ModelSerializer):
    photo_set = serializers.SerializerMethodField()
    plan_set = serializers.SerializerMethodField()
    group_set = serializers.SerializerMethodField()

    def get_photo_set(self, obj):
        photo = PhotoPage.objects.filter(diary_id=obj.id)
        serializer = DetailPhotoPageSerializer(photo, many=True)
        return serializer.data

    def get_plan_set(self, obj):
        plan = PlanPage.objects.filter(diary_id=obj.id)
        serializer = PlanSerializer(plan, many=True)
        return serializer.data

    def get_group_set(self, obj):
        group = UserGroup.objects.get(id=obj.group_id)
        serializer = GroupSerializer(group)
        return serializer.data

    class Meta:
        model = Note
        fields = [
            "id",
            "name",
            "group_set",
            "plan_set",
            "photo_set",
        ]


class PhotoPageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PhotoPage
        fields = "__all__"
        extra_kwargs = {
            "diary": {"required": False},
        }


class DetailPhotoPageSerializer(serializers.ModelSerializer):
    comment_set = serializers.SerializerMethodField()

    def get_comment_set(self, obj):
        comments = Comment.objects.filter(photo_id=obj.id)
        serializer = CommentSerializer(comments, many=True)
        return serializer.data

    class Meta:
        model = PhotoPage
        fields = "__all__"
        extra_kwargs = {
            "diary": {"required": False},
        }


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"
        extra_kwargs = {
            "photo": {"required": False},
            "user": {"required": False},
        }


class PlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlanPage
        fields = "__all__"
        extra_kwargs = {
            "diary": {"required": False},
        }


class StampPhotoSerializer(serializers.ModelSerializer):
    diary_id = serializers.IntegerField(source="diary.id")
    diary_name = serializers.CharField(source="diary.name")

    class Meta:
        model = PhotoPage
        fields = (
            "id",
            "location",
            "location_x",
            "location_y",
            "image",
            "created_at",
            "status",
            "diary_id",
            "diary_name",
        )


class StampSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stamp
        fields = "__all__"


class MarkerSerializer(serializers.ModelSerializer):
    photo = StampPhotoSerializer()

    class Meta:
        model = Stamp
        fields = "__all__"
