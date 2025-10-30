from django.urls import path
from .views import (
    ItineraryList, ItineraryDetail, ItineraryCreate,
    ItineraryUpdate, ItineraryDelete
)

app_name = "itineraries"
urlpatterns = [
    path("", ItineraryList.as_view(), name="list"),
    path("create/", ItineraryCreate.as_view(), name="create"),
    path("<slug:slug>/", ItineraryDetail.as_view(), name="detail"),
    path("<slug:slug>/edit/", ItineraryUpdate.as_view(), name="edit"),
    path("<slug:slug>/delete/", ItineraryDelete.as_view(), name="delete"),
]
