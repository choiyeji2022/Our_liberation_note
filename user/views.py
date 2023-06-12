import random
import string
from django.shortcuts import redirect
from json import JSONDecodeError
from django.http import HttpResponseRedirect, JsonResponse
import requests
import os

from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import EmailMessage
from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework import permissions, status
from rest_framework.authtoken.models import Token
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import AllowAny

from user.models import CheckEmail, User, UserGroup, OauthId
from user.serializers import (
    GroupCreateSerializer,
    GroupSerializer,
    LoginSerializer,
    SignUpSerializer,
    UserUpdateSerializer,
    UserViewSerializer,
    TokenObtainPairSerializer,
)

from allauth.socialaccount.models import SocialAccount
from dj_rest_auth.registration.views import SocialLoginView
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from allauth.socialaccount.providers.google import views as google_view
from allauth.socialaccount.providers.kakao import views as kakao_view


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
        user = User.objects.get(nickname=request.user)
        new_password = request.data.get("new_password")
        new_nickname = request.data.get("nickname")

        # 기존 비밀번호와 check_password가 일치할 경우 회원정보(닉네임, 비밀번호) 수정
        if user.check_password(check_password):
            serializer = UserUpdateSerializer(user, data=request.data, partial=True)
            if serializer.is_valid(raise_exception=True):
                # 비밀번호 변경한다면
                if new_password:
                    user.set_password(new_password)
                # 닉네임을 변경한다면
                if new_nickname:
                    user.nickname = new_nickname
                serializer.save()
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
        # 그룹장 여부 확인
        master = UserGroup.objects.filter(master=request.user).exists()
        # 그룹장이라면 활성화, 비활성화 상태 다 불러오기
        if master:
            groups = groups = UserGroup.objects.filter(status__in=["0", "1"]).order_by(
                "-created_at"
            )
        # 아니라면 활성화 상태만 불러오기
        else:
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
    permission_classes = [permissions.IsAuthenticated]

    # 그룹 상세보기
    def get(self, request, group_id):
        # 그룹장 여부 확인
        master = UserGroup.objects.filter(master=request.user).exists()
        # 그룹장이라면 활성화, 비활성화 상태 다 불러오기
        if master:
            group = get_object_or_404(
                UserGroup, Q(id=group_id) & Q(status__in=["0", "1"])
            )
        # 멤버라면 활성화 상태만 불러오기
        else:
            group = get_object_or_404(UserGroup, Q(id=group_id) & Q(status__in=["0"]))
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


# 소셜 로그인
BASE_URL = "http://127.0.0.1:8000/"


# 일반 소셜 로그인==============================

KAKAO_HOST= "https://kauth.kakao.com/"
class SocialUrlView(APIView):
    def post(self,request):
        social = request.data.get('social',None)
        if social is None:
            return Response({'error':'소셜로그인이 아닙니다'},status=status.HTTP_400_BAD_REQUEST)
        elif social == 'kakao':
            url = KAKAO_HOST + 'oauth/authorize?client_id=' + os.environ.get('KAKAO_REST_API_KEY') + '&redirect_uri=' + BASE_URL + '&response_type=code&prompt=login'
            return Response({'url':url},status=status.HTTP_200_OK)
        elif social == 'naver':
            # url = 'https://nid.naver.com/oauth2.0/authorize?response_type=code&client_id=' + os.environ.get('SOCIAL_AUTH_NAVER_CLIENT_ID') + '&redirect_uri=' + BASE_URL + '&state=' + os.environ.get("STATE")
            url = "https://nid.naver.com/oauth2.0/authorize?response_type=code&client_id="+ os.environ.get('SOCIAL_AUTH_NAVER_CLIENT_ID') + "&redirect_uri=" + BASE_URL + "&state=" + os.environ.get("STATE")
            return Response({'url':url},status=status.HTTP_200_OK)   
        elif social == 'google':
            # return Response({'key':os.environ.get('SOCIAL_AUTH_GOOGLE_CLIENT_ID'),'redirecturi':BASE_URL},status=status.HTTP_200_OK)
            client_id = os.environ.get('SOCIAL_AUTH_GOOGLE_CLIENT_ID')
            redirect_uri = BASE_URL
            
            url = f"https://accounts.google.com/o/oauth2/v2/auth?client_id={client_id}&redirect_uri={redirect_uri}&response_type=code&scope=email%20profile"
            
            return Response({'url': url}, status=status.HTTP_200_OK)
        
# ===============================================
class KakaoLoginView(APIView):
    def post(self,request):
        code = request.data.get('code')
        access_token = requests.post("https://kauth.kakao.com/"+"oauth/token",
            headers={"Content-Type":"application/x-www-form-urlencoded"},
            data={
                "grant_type":"authorization_code",
                "client_id":os.environ.get('KAKAO_REST_API_KEY'),
                "redirect_uri":"http://127.0.0.1:8000/",
                "code":code,
            },
        )
        access_token = access_token.json().get("access_token")
        user_data_request = requests.get("https://kapi.kakao.com/v2/user/me",
            headers={
                "Authorization": f"Bearer {access_token}",
                "Content-type": "application/x-www-form-urlencoded;charset=utf-8",
            },
        )
        user_datajson = user_data_request.json()
        user_data = user_datajson["kakao_account"]
        email = user_data["email"]
        nickname = user_data["profile"]["nickname"]
        try:
            user = User.objects.get(email=email)
            refresh = RefreshToken.for_user(user)
            refresh["email"] = user.email
            refresh["nickname"] = user.nickname
            return Response(
                {
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                },
                status=status.HTTP_200_OK
            )
        except:
            user = User.objects.create_user(email=email,nickname=nickname)
            user.set_unusable_password()
            user.save()
            refresh = RefreshToken.for_user(user)
            refresh["email"] = user.email
            refresh["nickname"] = user.nickname
            return Response(
                {
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                },
                status=status.HTTP_200_OK
            )

# ===============================================
class NaverLoginView(APIView):
    def post(self, request):
        code = request.data.get('code')
        client_id = os.environ.get('SOCIAL_AUTH_NAVER_CLIENT_ID')
        client_secret = os.environ.get('SOCIAL_AUTH_NAVER_SECRET')
        redirect_uri = "http://127.0.0.1:8000/"

        # 네이버 API로 액세스 토큰 요청
        access_token_request = requests.post("https://nid.naver.com/oauth2.0/token",
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
        user_data_request = requests.get("https://openapi.naver.com/v1/nid/me",
            headers={"Authorization": f"Bearer {access_token}",
                    "Content-Type": "application/json",
                    "Accept": "application/json",
                    },
        )

        user_data_json = user_data_request.json()
        print("1111", user_data_json)
        user_data = user_data_json.get("response")
        print(user_data)
        email = user_data.get("email")
        nickname = user_data.get("name")

        try:
            user = User.objects.get(email=email)
            refresh = RefreshToken.for_user(user)
            refresh["email"] = user.email
            refresh["name"] = user.nickname
            return Response(
                {
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                },
                status=status.HTTP_200_OK
            )
        except:
            user = User.objects.create_user(email=email, nickname=nickname)
            user.set_unusable_password()
            user.save()
            refresh = RefreshToken.for_user(user)
            refresh["email"] = user.email
            refresh["name"] = user.nickname
            return Response(
                {
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                },
                status=status.HTTP_200_OK
            )


# ===============================================

class GoogleLoginView(APIView):
    def post(self, request):
        code = request.data.get('code')
        # nickname = request.data.get('nickname')
        client_id = os.environ.get('SOCIAL_AUTH_GOOGLE_CLIENT_ID')
        client_secret = os.environ.get('SOCIAL_AUTH_GOOGLE_SECRET')
        redirect_uri = "http://127.0.0.1:8000/"

        # 구글 API로 액세스 토큰 요청
        access_token_request = requests.post("https://oauth2.googleapis.com/token",
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            data={
                "code": code,
                "client_id": client_id,
                "client_secret": client_secret,
                "redirect_uri": redirect_uri,
                "grant_type": "authorization_code",
                "scope": "email profile",
            }
        )
        access_token_json = access_token_request.json()
        access_token = access_token_json.get("access_token")

        # 구글 API로 사용자 정보 요청
        user_data_request = requests.get("https://www.googleapis.com/oauth2/v1/userinfo",
            headers={"Authorization": f"Bearer {access_token}"},
        )
        user_data_json = user_data_request.json()
        print(user_data_json)
        email = user_data_json.get("email")
        nickname = user_data_json.get("name")

        try:
            user = User.objects.get(email=email)
            refresh = RefreshToken.for_user(user)
            refresh["email"] = user.email
            refresh["nickname"] = user.nickname
            return Response(
                {
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                },
                status=status.HTTP_200_OK
            )
        except:
            user = User.objects.create_user(email=email, nickname=nickname)
            user.set_unusable_password()
            user.save()
            refresh = RefreshToken.for_user(user)
            refresh["email"] = user.email
            refresh["nickname"] = user.nickname
            return Response(
                {
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                },
                status=status.HTTP_200_OK
            )