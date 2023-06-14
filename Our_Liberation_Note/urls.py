from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("user/", include("user.urls")),
    path("note/", include("diary.urls")),
    path("test3/", include("diary.urls")),
]
