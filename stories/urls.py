from django.urls import path
from .views import (
    StoryList, StoryDetail, StoryCreate, StoryUpdate, StoryDelete, VoteToggle
)

app_name = "stories"

urlpatterns = [
    path("", StoryList.as_view(), name="list"),
    path("create/", StoryCreate.as_view(), name="create"),
    path("<slug:slug>/", StoryDetail.as_view(), name="detail"),
    path("<slug:slug>/edit/", StoryUpdate.as_view(), name="edit"),
    path("<slug:slug>/delete/", StoryDelete.as_view(), name="delete"),
    path("<slug:slug>/vote/", VoteToggle.as_view(), name="vote"),
]
