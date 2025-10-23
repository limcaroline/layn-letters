from django.urls import path
from . import views

app_name = "itineraries"

urlpatterns = [
    path("", views.itinerary_list_placeholder, name="list"),
]
