from django.urls import path

from . import views

urlpatterns = [
    path("success", views.success.as_view()),
    path("fail", views.fail),
    path(
        "api/subscription/",
        views.check_subscription.as_view(),
        name="check_subscription",
    ),
]
