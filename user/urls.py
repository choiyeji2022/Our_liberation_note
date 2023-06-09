from django.urls import path

from user import views

urlpatterns = [
    path("signup/", views.SignupView.as_view(), name="signup"),
    path("login/", views.LoginView.as_view(), name="login"),
    path("", views.UserView.as_view(), name="user_view"),  # 회원 정보
    path("sendemail/", views.SendEmail.as_view(), name="send_email"),  # 이메일 인증
    path(
        "changepassword/", views.ChangePassword.as_view(), name="changepassword"
    ),  # 비밀번호 재발급
    path("group/", views.GroupView.as_view(), name="group"),
    path("group/<int:group_id>/", views.GroupDetailView.as_view(), name="group"),
    path("my-page/", views.MyPageView.as_view(), name="my_page"),
    path("map/", views.MapView.as_view(), name="map"),
]
