from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView

from user.models import User, UserGroup
from user.serializers import (GroupCreateSerializer, GroupSerializer,
                              LoginSerializer, SignUpSerializer,
                              UserUpdateSerializer, UserViewSerializer)


# 회원 가입
class SignupView(APIView):
    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "해방일지 합류 완료!"}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 로그인
class LoginView(TokenObtainPairView):
    serializer_class = LoginSerializer
    pass


# 유저 정보
class UserView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    # 회원 정보 보기
    def get(self, request):
        return Response(UserViewSerializer(request.user).data)

    # 회원 정보 수정
    def patch(self, request):
        user = User.objects.get(nickname=request.user)
        serializer = UserUpdateSerializer(user, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({"message": "수정 완료!"}, status=status.HTTP_200_OK)
        else:
            return Response({serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    # 회원 삭제
    def delete(self, request):
        user = request.user
        user.is_active = False
        user.save()
        return Response({"message": "계정 삭제 완료!"})


class GroupView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        # 활성화된 그룹만 불러오기
        groups = UserGroup.objects.filter(status="0").order_by("-created_at")
        serializer = GroupSerializer(groups, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 그룹 만들기
    def post(self, request):
        serializer = GroupCreateSerializer(data=request.data)
        if serializer.is_valid():
            # 그룹 생성하면서 그룹장을 request.user로 설정
            group = serializer.save(master=request.user)
            # master를 멤버로 추가하기
            group.members.add(request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GroupDetailView(APIView):
    # 그룹 상세보기
    def get(self, request, group_id):
        # 활성, 비활성 다 불러오기
        group = get_object_or_404(UserGroup, Q(id=group_id) & Q(status__in=["0", "1"]))
        serializer = GroupSerializer(group)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 그룹 수정하기
    def patch(self, request, group_id):
        # 활성, 비활성 다 불러오기
        group = get_object_or_404(UserGroup, Q(id=group_id) & Q(status__in=["0", "1"]))
        # 본인이 생성한 그룹이 맞다면
        if request.user == group.master:
            serializer = GroupCreateSerializer(group, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        # 본인이 생성한 그룹이 아니라면
        else:
            return Response({"message": "권한이 없습니다."}, status=status.HTTP_403_FORBIDDEN)

    # 그룹 삭제하기
    def delete(self, request, group_id):
        # 활성, 비활성 다 불러오기
        group = get_object_or_404(UserGroup, Q(id=group_id) & Q(status__in=["0", "1"]))
        # 본인이 생성한 그룹이 맞다면
        if request.user == group.master:
            group.status = "3"
            group.save()
            return Response(
                {"message": "그룹이 삭제되었습니다."}, status=status.HTTP_204_NO_CONTENT
            )
        # 본인이 생성한 그룹이 아니라면
        else:
            return Response({"message": "권한이 없습니다."}, status=status.HTTP_403_FORBIDDEN)


class MyPageView(APIView):
    pass


class MapView(APIView):
    pass
