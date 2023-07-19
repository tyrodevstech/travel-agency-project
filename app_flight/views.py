from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic import TemplateView, FormView

# from django_filters.views import FilterView


from app_flight.models import AirPlaneTicketModel
from app_flight.filters import AirPlaneTicketFilters
# Create your views here.

class AirPlaneTicketsListView(ListView):
    model = AirPlaneTicketModel
    template_name = 'app_main/search.html'
    context_object_name = 'tickets'


    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = AirPlaneTicketFilters(self.request.GET, queryset=queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.filterset.form
        return context

class AirPlaneTicketsDetailsView(TemplateView):
    template_name = 'app_flight/airplane_tickets.html'


class AirPlaneTicketsPaymentsView(TemplateView):
    template_name = 'app_flight/payment.html'