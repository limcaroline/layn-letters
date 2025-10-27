from django.urls import path
from .views import (
    ReviewList, ReviewDetail, ReviewCreate, ReviewUpdate, ReviewDelete,
    PlaceCreate, ReviewCommentEdit, ReviewCommentDelete,
    ReviewCommentVoteToggle,
)

app_name = "reviews"

urlpatterns = [
    path("", ReviewList.as_view(), name="list"),
    path("create/", ReviewCreate.as_view(), name="create"),
    path("<int:pk>/", ReviewDetail.as_view(), name="detail"),
    path("<int:pk>/edit/", ReviewUpdate.as_view(), name="edit"),
    path("<int:pk>/delete/", ReviewDelete.as_view(), name="delete"),
    path("place/create/", PlaceCreate.as_view(), name="place_create"),
    path("comment/<int:pk>/edit/", ReviewCommentEdit.as_view(),
         name="comment_edit"),
    path("comment/<int:pk>/delete/", ReviewCommentDelete.as_view(),
         name="comment_delete"),
    path("comment/<int:pk>/vote/", ReviewCommentVoteToggle.as_view(),
         name="comment_vote"),
]
