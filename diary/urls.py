from django.urls import path

from diary import views

urlpatterns = [
    path("", views.NoteView.as_view(), name="note_view"),
    path("<int:note_id>", views.NoteView.as_view(), name="note_delete"),
    path("photo/<int:note_id>", views.PhotoPageView.as_view(), name="photo_page"),
    path(
        "photo-detail/<int:photo_id>",
        views.DetailPhotoPageView.as_view(),
        name="detail_photo_page",
    ),
    path(
        "plan-detail/<int:plan_id>",
        views.DetailPlanPageView.as_view(),
        name="detail_plan_page",
    ),
    path("comment/<int:comment_id>", views.CommentView.as_view(), name="comment"),
    path("trash", views.Trash.as_view(), name="trash"),
    path("stamp", views.StampView.as_view(), name="stamp"),
]
# 활성화, 비 활성화, 강제 중지, 삭제(복구 요청 때문에 영구 삭제는 잘 안함)
