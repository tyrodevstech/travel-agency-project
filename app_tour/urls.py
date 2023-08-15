from django.urls import path
from app_tour.views import *

app_name = "app_tour"


urlpatterns = [
    path("tour-list/", TourIndexView.as_view(), name="tour_list"),
    path("tour-details/<int:pk>", TourDetailsView.as_view(), name="tour_details"),
    path("tour-payments/<int:pk>", TourPaymentsView.as_view(), name="tour_payments"),
]