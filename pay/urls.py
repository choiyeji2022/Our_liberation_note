from django.urls import path

from . import views

urlpatterns = [
    path("success", views.Success.as_view(), name="success"),  # 결제 저장
    path("fail", views.fail),  # 결제 실패l
    path(
        "subscription/<int:note_id>",  # 구독 여부 확인
        views.check_subscription.as_view(),
        name="check_subscription",
    ),
]
