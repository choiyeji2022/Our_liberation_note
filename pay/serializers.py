from rest_framework import serializers
from rest_framework.serializers import ValidationError

from .models import Payment, Subscribe


class SubscribeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscribe
        fields = "__all__"
