from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView


class SignupView(APIView):
    pass


class LoginView(TokenObtainPairView):
    # serializer_class = LoginSerializer
    pass

class GroupView(APIView):
    pass


class MyPageView(APIView):
    pass


class MapView(APIView):
    pass