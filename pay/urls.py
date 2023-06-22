from django.urls import path

from . import views

urlpatterns = [
    path("success", views.success.as_view(), name='success'),
    path("fail", views.fail),
]
