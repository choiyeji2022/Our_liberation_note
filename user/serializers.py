from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from user.models import User


class SignUpSerializer(serializers.ModelSerializer):
    join_date = serializers.SerializerMethodField()
    
    def get_join_date(self, obj):
        return obj.join_date.strftime("%Y년 %m월 %d일 %p %I:%M")
    class Meta:
        model = User
        fields = "__all__"
        
    def create(self, validated_data):
        user = super().create(validated_data)
        password = user.password
        user.set_password(password)
        user.save()
        return user


class LoginSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['nickname'] = user.nickname
        token['email'] = user.email
        token['is_admin'] = user.is_admin

        return token
    
class UserViewSerializer(serializers.ModelSerializer):
    join_date = serializers.SerializerMethodField()
    
    def get_join_date(self, obj):
        return obj.join_date.strftime("%Y년 %m월 %d일 %p %I:%M")
    class Meta:
        model = User
        exclude = ('password',)
        
class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("nickname","email", "password")
        
    def update(self,instance, validated_data):
        user = super().update(instance,validated_data)
        password = user.password
        user.set_password(password)
        user.save()
        return user