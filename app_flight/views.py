from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic.list import ListView
from django.views.generic import TemplateView, FormView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

# from django_filters.views import FilterView


from app_flight.models import AirPlaneTicketModel
from app_flight.filters import AirPlaneTicketFilters


from app_main.forms import UserFeedbackForm
# Create your views here.

signin_decorators = [login_required(login_url="app_main:signin")]



class AirPlaneTicketsListView(ListView):
    model = AirPlaneTicketModel
    template_name = 'app_main/search.html'
    context_object_name = 'tickets'


    def get_queryset(self):
        queryset = super().get_queryset()
        filter_data = self.request.GET.copy()
        # ticket_price_min = float(filter_data.get('ticket_price_min')) if filter_data.get('ticket_price_min') else None
        # traveler = filter_data.get('traveler',1)
        # if int(traveler) > 1 and ticket_price_min:
        #     filter_data['ticket_price_min'] = ticket_price_min * int(traveler)
            
        # print(filter_data)

        self.filterset = AirPlaneTicketFilters(filter_data, queryset=queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter_form'] = self.filterset.form
        context['schedule'] = self.request.GET.getlist('schedule')
        context['traveler'] = self.request.GET.get('traveler',1)

        return context




@method_decorator(signin_decorators, name="dispatch")
class AirPlaneTicketsDetailsView(FormView):
    template_name = 'app_flight/airplane_tickets.html'
    form_class = UserFeedbackForm
    # success_url = reverse_lazy("app_book:home")


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs.get('pk')
        context['ticket'] = get_object_or_404(AirPlaneTicketModel, id=pk)
        return context




@method_decorator(signin_decorators, name="dispatch")
class AirPlaneTicketsPaymentsView(TemplateView):
    template_name = 'app_flight/payment.html'