from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework import serializers
from rest_framework.serializers import ValidationError

from user.models import UserGroup
from user.serializers import GroupSerializer

from .models import Comment, Note, PhotoPage, PlanPage, Stamp
from .validators import check_words


# 노트 일반 CRUD
class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = "__all__"

    def validate(self, attrs):
        if check_words(attrs["name"]):
            raise ValidationError("비속어 사용이 불가합니다!")
        return attrs


# 노트에 들어 가는 모든 photo, Plan
class DetailNoteSerializer(serializers.ModelSerializer):
    photo_set = serializers.SerializerMethodField()
    plan_set = serializers.SerializerMethodField()
    group_set = serializers.SerializerMethodField()

    def get_photo_set(self, obj):
        photo = PhotoPage.objects.filter(diary_id=obj.id, status=0)
        serializer = DetailPhotoPageSerializer(photo, many=True)
        return serializer.data

    def get_plan_set(self, obj):
        plan = PlanPage.objects.filter(diary_id=obj.id, status=0)
        serializer = PlanSerializer(plan, many=True)
        return serializer.data

    def get_group_set(self, obj):
        group = UserGroup.objects.get(id=obj.group_id, status=0)
        serializer = GroupSerializer(group)
        return serializer.data

    class Meta:
        model = Note
        fields = [
            "id",
            "name",
            "group",
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


class PatchPhotoPageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PhotoPage
        exclude = ["image"]
        extra_kwargs = {
            "diary": {"required": False},
        }


class DetailPhotoPageSerializer(serializers.ModelSerializer):
    comment_set = serializers.SerializerMethodField()

    def get_comment_set(self, obj):
        comments = Comment.objects.filter(photo_id=obj.id, status=0)
        serializer = CommentSerializer(comments, many=True)
        return serializer.data

    class Meta:
        model = PhotoPage
        fields = "__all__"
        extra_kwargs = {
            "diary": {"required": False},
        }


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.EmailField(source="user.email", read_only=True)

    class Meta:
        model = Comment
        fields = "__all__"
        extra_kwargs = {
            "photo": {"required": False},
            "user": {"required": False},
        }

    def validate(self, attrs):
        if check_words(attrs["comment"]):
            raise ValidationError("비속어 사용이 불가합니다!")
        if len(attrs["comment"]) > 30:
            raise ValidationError("30자 이하로 작성해주세요!")
        return attrs


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
    group_name = serializers.CharField(source="diary.group.name")

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
            "group_name",
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
