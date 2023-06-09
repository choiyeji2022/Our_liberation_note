from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("allauth.urls")),
    path("user/", include("user.urls")),
    path("note/", include("diary.urls")),
]
