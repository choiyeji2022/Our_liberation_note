from django.urls import path

from . import views

urlpatterns = [
    path("success", views.Success.as_view(), name="success"),
    path("fail", views.fail),
    path(
        "subscription/<int:note_id>",
        views.check_subscription.as_view(),
        name="check_subscription",
    ),
]
