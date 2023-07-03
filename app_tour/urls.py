from django.urls import path
from app_tour.views import *

app_name = "app_tour"


urlpatterns = [
    path("tour-home/", TourIndexView.as_view(), name="tour_home"),
]