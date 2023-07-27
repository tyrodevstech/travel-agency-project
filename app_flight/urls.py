from django.urls import path
from app_flight.views import *

app_name = "app_flight"


urlpatterns = [
    path("tickets-list/", AirPlaneTicketsListView.as_view(), name="tickets_list"),
    path("tickets-details/<int:pk>/", AirPlaneTicketsDetailsView.as_view(), name="tickets_details"),
    path("tickets-payments/", AirPlaneTicketsPaymentsView.as_view(), name="tickets_payments"),
]