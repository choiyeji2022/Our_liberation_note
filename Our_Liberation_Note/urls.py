from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    # path("user/", include("allauth.urls")), # 소셜 로그인
    path("user/", include("user.urls")),
    path("note/", include("diary.urls")),
]
