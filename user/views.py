from rest_framework.views import APIView
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from user.serializers import LoginSerializer, SignUpSerializer, UserViewSerializer, UserUpdateSerializer
from user.models import User
from rest_framework import status, permissions


# 회원 가입
class SignupView(APIView):
     def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message":"해방일지 합류 완료!"}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# 로그인
class LoginView(TokenObtainPairView):
    serializer_class = LoginSerializer
    pass

# 유저 정보
class UserView(APIView):
    permission_classes=[permissions.IsAuthenticated]
    # 회원 정보 보기
    def get(self, request):
        return Response(UserViewSerializer(request.user).data)
    
    # 회원 정보 수정
    def patch(self, request):
        user = User.objects.get(nickname=request.user)
        serializer = UserUpdateSerializer(
            user, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({'message': '수정 완료!'}, status=status.HTTP_200_OK)
        else:
            return Response({serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    # 회원 삭제
    def delete(self, request):
        user= request.user
        user.is_active = False
        user.save()
        return Response({'message': '계정 삭제 완료!'})

class GroupView(APIView):
    pass


class MyPageView(APIView):
    pass


class MapView(APIView):
    pass