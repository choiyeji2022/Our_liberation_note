from rest_framework import serializers
from .models import Payment, Subscribe
from rest_framework.serializers import ValidationError


class SubscribeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Subscribe
        fields = ('__all__')
