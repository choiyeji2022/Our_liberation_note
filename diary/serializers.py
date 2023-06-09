from rest_framework import serializers

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
