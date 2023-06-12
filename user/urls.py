from django.urls import path

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
    path(
        "changepassword/", views.ChangePassword.as_view(), name="changepassword"
    ),
    
    # 그룹
    path("group/", views.GroupView.as_view(), name="group"),
    path("group/<int:group_id>/", views.GroupDetailView.as_view(), name="group"),
    path("my-page/", views.MyPageView.as_view(), name="my_page"),
    path("map/", views.MapView.as_view(), name="map"),
    
    # 카카오 로그인
    # path('kakao/login/', views.kakao_login, name='kakao_login'),
    # path('kakao/callback/', views.kakao_callback, name='kakao_callback'),
    # path('kakao/login/finish/', views.KakaoLogin.as_view(), name='kakao_login_todjango'),
    # # 구글 로그인
    # path('google/login/', views.google_login, name='google_login'),
    # path('google/callback/', views.google_callback, name='google_callback'),
    # path('google/login/finish/', views.GoogleLogin.as_view(), name='google_login_todjango'),
    # 네이버 로그인
    # path('naver/login', views.naver_login, name='naver_login'),
    # path('naver/callback/', views.naver_callback, name='naver_callback'),
    # path('naver/login/finish/', views.NaverLogin.as_view(), name='naver_login_todjango'),
    
    path('social/', views.SocialUrlView.as_view(), name='social_login'),
    path('kakao/', views.KakaoLoginView.as_view(), name='kakao_login'),
    path('naver/', views.NaverLoginView.as_view(), name='naver_login'),
    path('google/', views.GoogleLoginView.as_view(), name='google_login'),
]
