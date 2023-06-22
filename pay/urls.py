from django.urls import path

from . import views

urlpatterns = [
    path("success", views.Success.as_view(), name="success"),
    path("fail", views.fail),
]
