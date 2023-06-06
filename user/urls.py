from django.urls import path
from user import views

urlpatterns = [
    path('signup/', views.SignupView.as_view(), name='signup'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('group/', views.GroupView.as_view(), name='group'),
    path('my-page/', views.MyPageView.as_view(), name='my_page'),
    path('map/', views.MapView.as_view(), name='map'),
]
