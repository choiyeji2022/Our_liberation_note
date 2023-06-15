import os
import random
import string
from django.http import QueryDict
import requests
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import EmailMessage
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

from diary.models import Stamp
from diary.serializers import StampSerializer
from user.models import CheckEmail, User, UserGroup
from user.serializers import (GroupCreateSerializer, GroupSerializer,
                              LoginSerializer, SignUpSerializer,
                              TokenObtainPairSerializer, UserUpdateSerializer,
                              UserViewSerializer)


# 이메일 전송
class SendEmail(APIView):
    def post(self, request):
        subject = "인증 번호를 확인해주세요."
        email = request.data.get("email")
        random_code = "".join(
            random.choices(string.ascii_uppercase + string.digits, k=6)
        )  # 6자리 랜덤 문자열 생성
        body = f"이메일 확인 코드: {random_code}"  # 랜덤 코드 본문에 추가
        email = EmailMessage(
            subject,
            body,
            to=[email],
        )
        email.send()

        # 인증 코드 DB에 저장
        code = CheckEmail.objects.create(code=random_code, email=email)

        return Response(
            {"message": "이메일을 전송했습니다. 메일함을 확인하세요.", "code": code.id},
            status=status.HTTP_200_OK,
        )


# 회원 가입
class SignupView(APIView):
    def post(self, request):
        email = request.data.get("email")
        code = request.data.get("code")

        # 이메일 중복 확인
        try:
            user = User.objects.get(email=email)
            return Response(
                {"message": "이메일이 이미 존재합니다."}, status=status.HTTP_400_BAD_REQUEST
            )
        except ObjectDoesNotExist:
            pass
        # 인증 코드 일치하는지 확인
        try:
            code_obj = CheckEmail.objects.get(code=code)
        except CheckEmail.DoesNotExist:
            return Response(
                {"message": "이메일 확인 코드가 유효하지 않습니다."}, status=status.HTTP_400_BAD_REQUEST
            )

        serializer = SignUpSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            code_obj.delete()  # 이메일 확인 코드 삭제
            return Response({"message": "가입완료!"}, status=status.HTTP_201_CREATED)
        else:
            return Response(
                {"message": f"{serializer.errors}"}, status=status.HTTP_400_BAD_REQUEST
            )


# 로그인
class LoginView(TokenObtainPairView):
    serializer_class = LoginSerializer


# 유저 정보
class UserView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    # 회원 정보 보기
    def get(self, request):
        return Response(UserViewSerializer(request.user).data)

    # 회원 정보 수정
    def patch(self, request):
        check_password = request.data.get("check_password")
        user = User.objects.get(email=request.user)
        new_password = request.data.get("new_password")

        if new_password == "":
            return Response({'message':'변경할 비밀번호를 입력해주세요!'}, status=status.HTTP_400_BAD_REQUEST)
        # 기존 비밀번호와 check_password가 일치할 경우 회원정보(닉네임, 비밀번호) 수정
        if check_password and user.check_password(check_password):
            serializer = UserUpdateSerializer(user, data=request.data, partial=True)
            if serializer.is_valid(raise_exception=True):
                # 비밀번호 변경한다면
                if new_password:
                    user.set_password(new_password)

                user.save()
                return Response({"message": "수정 완료!"}, status=status.HTTP_200_OK)
            else:
                return Response({serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(
                {"message": "비밀번호가 일치하지 않습니다"}, status=status.HTTP_400_BAD_REQUEST
            )

    # 회원 삭제
    def delete(self, request):
        user = request.user
        user.is_active = False
        user.save()
        return Response({"message": "계정 삭제 완료!"})


# 비밀번호 새로 만들기
class ChangePassword(APIView):
    def post(self, request):
        email = request.data.get("email")
        code = request.data.get("code")
        new_password = request.data.get("new_password")

        # 인증 코드 일치하는지 확인
        try:
            code_obj = CheckEmail.objects.get(code=code)
        except CheckEmail.DoesNotExist:
            return Response(
                {"message": "이메일 확인 코드가 유효하지 않습니다."}, status=status.HTTP_400_BAD_REQUEST
            )

        # 이메일 일치하는지 확인
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response(
                {"message": "비밀번호 찾기를 위한 이메일이 일치하지 않습니다."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # 비밀번호 업데이트
        user.set_password(new_password)
        user.save()

        # 인증코드 삭제
        code_obj.delete()
        return Response({"message": "비밀번호 변경 완료!"}, status=status.HTTP_200_OK)


class GroupView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        groups = UserGroup.objects.filter(members=request.user, status="0").order_by(
            "-created_at"
        )
        serializer = GroupSerializer(groups, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 그룹 만들기
    def post(self, request):
        serializer = GroupCreateSerializer(data=request.data)
        if serializer.is_valid():
            group_name = serializer.validated_data.get("name")
            # 이미 같은 이름의 그룹이 있는지 확인
            if UserGroup.objects.filter(name=group_name).exists():
                error_message = {"error": "이미 같은 이름의 그룹이 존재합니다."}
                return Response(error_message, status=status.HTTP_400_BAD_REQUEST)
            # 그룹 생성하면서 그룹장을 request.user로 설정
            group = serializer.save(master_id=request.user.id)
            # master를 멤버로 추가하기
            group.members.add(request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GroupDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    # 그룹 상세보기
    def get(self, request, group_id):
        group = get_object_or_404(
            UserGroup.objects.filter(id=group_id, members=request.user, status="0")
        )
        serializer = GroupSerializer(group)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 그룹 수정하기
    def patch(self, request, group_id):
        group = get_object_or_404(
            UserGroup.objects.filter(id=group_id, master_id=request.user.id, status="0")
        )
        # 본인이 생성한 그룹이 맞다면
        if request.user.id == group.master_id:
            serializer = GroupCreateSerializer(group, data=request.data, partial=True)
            if serializer.is_valid():
                new_name = serializer.validated_data.get("name")
                # 그룹명 중복 확인
                if (
                    UserGroup.objects.filter(name=new_name)
                    .exclude(id=group_id)
                    .exists()
                ):
                    return Response(
                        {"message": "같은 이름의 그룹이 이미 존재합니다."},
                        status=status.HTTP_400_BAD_REQUEST,
                    )

                # 수정하면서 그룹장을 request.user로 설정
                group = serializer.save(master_id=request.user.id)
                # master를 멤버로 추가하기
                group.members.add(request.user)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        # 본인이 생성한 그룹이 아니라면
        else:
            return Response({"message": "권한이 없습니다."}, status=status.HTTP_403_FORBIDDEN)

    # 그룹 삭제하기
    def delete(self, request, group_id):
        # 활성, 비활성 다 불러오기
        group = get_object_or_404(
            UserGroup.objects.filter(id=group_id, master_id=request.user.id, status="0")
        )
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


# 소셜 로그인
URI = "http://127.0.0.1:5500/"


# OAuth 인증 url
class SocialUrlView(APIView):
    def post(self, request):
        social = request.data.get("social", None)
        code = request.data.get("code", None)
        if social is None:
            return Response(
                {"error": "소셜로그인이 아닙니다"}, status=status.HTTP_400_BAD_REQUEST
            )
        elif social == "kakao":
            url = (
                "https://kauth.kakao.com/oauth/authorize?client_id="
                + os.environ.get("KAKAO_REST_API_KEY")
                + "&redirect_uri="
                + URI
                + "&response_type=code&prompt=login"
            )
            return Response({"url": url}, status=status.HTTP_200_OK)
        elif social == "naver":
            url = (
                "https://nid.naver.com/oauth2.0/authorize?response_type=code&client_id="
                + os.environ.get("SOCIAL_AUTH_NAVER_CLIENT_ID")
                + "&redirect_uri="
                + URI
                + "&state="
                + os.environ.get("STATE")
            )
            return Response({"url": url}, status=status.HTTP_200_OK)
        elif social == "google":
            client_id = os.environ.get("SOCIAL_AUTH_GOOGLE_CLIENT_ID")
            redirect_uri = URI

            url = f"https://accounts.google.com/o/oauth2/v2/auth?client_id={client_id}&redirect_uri={redirect_uri}&response_type=code&scope=email%20profile"

            return Response({"url": url}, status=status.HTTP_200_OK)


# 카카오 소셜 로그인
class KakaoLoginView(APIView):
    def post(self, request):
        code = request.data.get("code")
        access_token = requests.post(
            "https://kauth.kakao.com/" + "oauth/token",
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            data={
                "grant_type": "authorization_code",
                "client_id": os.environ.get("KAKAO_REST_API_KEY"),
                "redirect_uri": URI,
                "code": code,
            },
        )
        access_token = access_token.json().get("access_token")
        user_data_request = requests.get(
            "https://kapi.kakao.com/v2/user/me",
            headers={
                "Authorization": f"Bearer {access_token}",
                "Content-type": "application/x-www-form-urlencoded;charset=utf-8",
            },
        )
        user_datajson = user_data_request.json()
        user_data = user_datajson["kakao_account"]
        email = user_data["email"]
        try:
            user = User.objects.get(email=email)
            refresh = RefreshToken.for_user(user)
            refresh["email"] = user.email
            return Response(
                {
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                },
                status=status.HTTP_200_OK,
            )
        except:
            user = User.objects.create_user(email=email)
            user.set_unusable_password()
            user.save()
            refresh = RefreshToken.for_user(user)
            refresh["email"] = user.email
            return Response(
                {
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                },
                status=status.HTTP_200_OK,
            )


# 네이버 소셜 로그인
class NaverLoginView(APIView):
    def post(self, request):
        code = request.data.get("code")
        client_id = os.environ.get("SOCIAL_AUTH_NAVER_CLIENT_ID")
        client_secret = os.environ.get("SOCIAL_AUTH_NAVER_SECRET")
        redirect_uri = URI

        # 네이버 API로 액세스 토큰 요청
        access_token_request = requests.post(
            "https://nid.naver.com/oauth2.0/token",
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            data={
                "grant_type": "authorization_code",
                "client_id": client_id,
                "client_secret": client_secret,
                "redirect_uri": redirect_uri,
                "code": code,
            },
        )

        access_token_json = access_token_request.json()
        access_token = access_token_json.get("access_token")

        # 네이버 API로 사용자 정보 요청
        user_data_request = requests.get(
            "https://openapi.naver.com/v1/nid/me",
            headers={
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json",
                "Accept": "application/json",
            },
        )

        user_data_json = user_data_request.json()
        print("1111", user_data_json)
        user_data = user_data_json.get("response")
        print("user_data", user_data)
        email = user_data.get("email")

        try:
            user = User.objects.get(email=email)
            refresh = RefreshToken.for_user(user)
            refresh["email"] = user.email
            return Response(
                {
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                },
                status=status.HTTP_200_OK,
            )
        except:
            user = User.objects.create_user(email=email)
            user.set_unusable_password()
            user.save()
            refresh = RefreshToken.for_user(user)
            refresh["email"] = user.email
            return Response(
                {
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                },
                status=status.HTTP_200_OK,
            )


# 구글 소셜 로그인
class GoogleLoginView(APIView):
    def post(self, request):
        code = request.data.get("code")
        # nickname = request.data.get('nickname')
        client_id = os.environ.get("SOCIAL_AUTH_GOOGLE_CLIENT_ID")
        client_secret = os.environ.get("SOCIAL_AUTH_GOOGLE_SECRET")
        redirect_uri = URI

        # 구글 API로 액세스 토큰 요청
        access_token_request = requests.post(
            "https://oauth2.googleapis.com/token",
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            data={
                "code": code,
                "client_id": client_id,
                "client_secret": client_secret,
                "redirect_uri": redirect_uri,
                "grant_type": "authorization_code",
                "scope": "email",
            },
        )
        access_token_json = access_token_request.json()
        access_token = access_token_json.get("access_token")

        # 구글 API로 사용자 정보 요청
        user_data_request = requests.get(
            "https://www.googleapis.com/oauth2/v1/userinfo",
            headers={"Authorization": f"Bearer {access_token}"},
        )
        user_data_json = user_data_request.json()
        print(user_data_json)
        email = user_data_json.get("email")

        try:
            user = User.objects.get(email=email)
            refresh = RefreshToken.for_user(user)
            refresh["email"] = user.email
            return Response(
                {
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                },
                status=status.HTTP_200_OK,
            )
        except:
            user = User.objects.create_user(email=email)
            user.set_unusable_password()
            user.save()
            refresh = RefreshToken.for_user(user)
            refresh["email"] = user.email
            return Response(
                {
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                },
                status=status.HTTP_200_OK,
            )


class MyPageView(APIView):
    def get(self, request, user_id):
        profile = get_object_or_404(User, id=user_id)
        stamp = Stamp.objects.filter(user=user_id)
        group = UserGroup.objects.filter(Q(members=user_id) | Q(master=user_id))
        profileserializer = UserViewSerializer(profile)
        stampserializer = StampSerializer(stamp, many=True)
        groupSerializer = GroupSerializer(group, many=True)
        data = {
            "profile": profileserializer.data,
            "stamps": stampserializer.data,
            "groups": groupSerializer.data,
        }
        return Response(data, status=status.HTTP_200_OK)
