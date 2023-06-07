from rest_framework.views import APIView
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from user.serializers import LoginSerializer, SignUpSerializer

class SignupView(APIView):
     def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message":"해방일지 합류 완료!"}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(TokenObtainPairView):
    serializer_class = LoginSerializer
    pass

class GroupView(APIView):
    pass


class MyPageView(APIView):
    pass


class MapView(APIView):
    pass