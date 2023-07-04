from django.urls import path
from app_tour.views import *

app_name = "app_tour"


urlpatterns = [
    path("tour-list/", TourIndexView.as_view(), name="tour_list"),
    path("tour-details/", TourDetailsView.as_view(), name="tour_details"),
]