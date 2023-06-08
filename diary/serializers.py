from rest_framework.serializers import ValidationError
from rest_framework import serializers
from .models import PhotoPage, Comment 

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