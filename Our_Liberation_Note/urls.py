from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static
from Our_Liberation_Note import settings

urlpatterns = [
    path("admin/", admin.site.urls),
    path("user/", include("user.urls")),
    path("note/", include("diary.urls")),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
