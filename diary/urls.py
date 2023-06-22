from django.conf.urls.static import static
from django.urls import path

from diary import views
from Our_Liberation_Note import settings

urlpatterns = [
    path("", views.NoteView.as_view(), name="note_post"),
    path("<int:group_id>", views.NoteView.as_view(), name="note_detail"),
    path(
        "photo/<int:note_id>/<int:offset>",
        views.PhotoPageView.as_view(),
        name="photo_page_get",
    ),
    path("photo/<int:note_id>", views.PhotoPageView.as_view(), name="photo_page_post"),
    path("plan/<int:note_id>", views.PlanPageView.as_view(), name="plan_page"),
    path(
        "note-detail/<int:note_id>",
        views.DetailNoteView.as_view(),
        name="detail_note",
    ),
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
    path(
        "comment/<int:photo_id>/<int:comment_id>",
        views.CommentView.as_view(),
        name="comment",
    ),
    path("trash", views.Trash.as_view(), name="trash"),
    path("trash/<int:pk>", views.Trash.as_view(), name="trash"),
    path("stamp/<int:photo_id>", views.StampView.as_view(), name="stamp"),
    path(
        "markerstamps/<str:photo_location>",
        views.MarkerStampsView.as_view(),
        name="markerstamps",
    ),
    path("search", views.SearchDestination.as_view(), name="search"),
    path("email/<int:note_id>", views.EmailView.as_view(), name="email"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
