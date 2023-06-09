from rest_framework.serializers import ValidationError
from rest_framework import serializers
from .models import Comment, Note, Photo, PhotoPage, PlanPage, Stamp 
from diary.models import Note


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
        fields = '__all__'
        

class DetailPhotoPageSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = PhotoPage
        fields = '__all__'
    
class CommentSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Comment
        fields = '__all__'


class PlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlanPage
        fields = "__all__"
        extra_kwargs = {
            "note": {"required": False},
        }

