from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from user import views

urlpatterns = [
    # 로그인
    path("signup/", views.SignupView.as_view(), name="signup"),
    path("login/", views.LoginView.as_view(), name="login"),
    # 회원 정보
    path("", views.UserView.as_view(), name="user_view"),
    # 이메일 인증
    path("sendemail/", views.SendEmail.as_view(), name="send_email"),
    # 비밀번호 재발급
    path("changepassword/", views.ChangePassword.as_view(), name="changepassword"),
    # 그룹
    path("group/", views.GroupView.as_view(), name="group"),
    path("group/<int:group_id>/", views.GroupDetailView.as_view(), name="group_detail"),
    # 소셜 로그인
    path("social/", views.SocialUrlView.as_view(), name="social_login"),
    path("kakao/", views.KakaoLoginView.as_view(), name="kakao_login"),
    path("naver/", views.NaverLoginView.as_view(), name="naver_login"),
    path("google/", views.GoogleLoginView.as_view(), name="google_login"),
    path("my-page/", views.MyPageView.as_view(), name="my_page"),
    # 유저 정보 리스트
    path("userlist/", views.UserListView.as_view(), name="user_list"),
]
