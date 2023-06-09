from rest_framework import serializers
from rest_framework.serializers import ValidationError

from .models import Comment, Note, PhotoPage, PlanPage, Stamp


class NoteSerializer(serializers.ModelSerializer):
    created_at = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()
    # 그룹 불러오기 추후 수정
    # group_set = GroupListserializer(many=True)

    class Meta:
        model = Note
        fields = "__all__"


class NoteCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = (
            "name",
            "category",
        )


class PhotoPageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PhotoPage
        fields = "__all__"
        extra_kwargs = {
            "diary": {"required": False},
        }


class DetailPhotoPageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PhotoPage
        fields = "__all__"


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"
        extra_kwargs = {
            "photo": {"required": False},
        }


class PlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlanPage
        fields = "__all__"
        extra_kwargs = {
            "note": {"required": False},
        }
