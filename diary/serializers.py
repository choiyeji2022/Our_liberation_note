from rest_framework import serializers
from rest_framework.serializers import ValidationError

from .models import Comment, Note, Photo, PhotoPage, PlanPage, Stamp


class PlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlanPage
        fields = "__all__"
        extra_kwargs = {
            "note": {"required": False},
        }
