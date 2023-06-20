from rest_framework import serializers
from rest_framework.serializers import ValidationError
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from user.models import User, UserGroup

from .validators import check_words


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
        token["email"] = user.email
        token["is_admin"] = user.is_admin

        return token


class UserViewSerializer(serializers.ModelSerializer):
    join_date = serializers.SerializerMethodField()

    def get_join_date(self, obj):
        return obj.join_date.strftime("%Y년 %m월 %d일 %p %I:%M")

    class Meta:
        model = User
        exclude = ("password",)


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("password", "email")

    def update(self, instance, validated_data):
        # 새로운 비밀번호로 설정
        password = validated_data.get("new_password")
        if password:
            instance.set_password(password)

        instance.save()
        return instance


class GroupSerializer(serializers.ModelSerializer):
    master = serializers.SerializerMethodField()
    members = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()
    created_at = serializers.SerializerMethodField()
    updated_at = serializers.SerializerMethodField()

    def get_master(self, obj):
        return obj.master.email

    def get_members(self, obj):
        return ", ".join(
            obj.members.values_list("email", flat=True)
        )  # values_list는 member 필드의 값을 리스트로 반환, flat을 쓰지 않으면 튜플로 반환

    def get_status(self, obj):
        if obj.status == "0":
            return "활성화"
        elif obj.status == "1":
            return "비활성화"
        elif obj.status == "2":
            return "강제중지"
        elif obj.status == "3":
            return "삭제"

    def get_created_at(self, obj):
        return obj.created_at.strftime("%Y년 %m월 %d일 %p %I:%M")

    def get_updated_at(self, obj):
        return obj.updated_at.strftime("%Y년 %m월 %d일 %p %I:%M")

    class Meta:
        model = UserGroup
        fields = "__all__"


class GroupCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserGroup
        fields = ("name", "members", "master", "status")
        read_only_fields = ("master",)

    def validate(self, attrs):
        if check_words(attrs["name"]):
            raise ValidationError("비속어 사용이 불가합니다!")
        return attrs


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("email",)
