from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.views.generic import FormView, TemplateView
from django.views.generic.list import ListView
from django.forms import formset_factory
from app_flight.filters import AirPlaneTicketFilters
from app_flight.models import AirplaneTicket, Order, OrderFlight
from app_main.forms import UserFeedbackForm

from .forms import OrderFlightForm, FlightPaymentsForm

# from django_filters.views import FilterView


# Create your views here.

signin_decorators = [login_required(login_url="app_main:signin")]


class AirPlaneTicketsListView(ListView):
    model = AirplaneTicket
    template_name = "app_flight/flights.html"
    context_object_name = "tickets"

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
        context["filter_form"] = self.filterset.form
        context["schedule"] = self.request.GET.getlist("schedule")
        request = self.request
        traveler_adult = int(request.GET.get("traveler_adult", 1))
        traveler_child = int(request.GET.get("traveler_child", 0))
        traveler_infant = int(request.GET.get("traveler_infant", 0))
        context["traveler_adult"] = traveler_adult
        context["traveler_child"] = traveler_child
        context["traveler_infant"] = traveler_infant
        context["total_traveler"] = traveler_adult + traveler_child + traveler_infant

        ticket_query_params = self.request.GET.dict()
        self.request.session["ticket_query_params"] = ticket_query_params

        return context


@method_decorator(signin_decorators, name="dispatch")
class AirPlaneTicketsDetailsView(FormView):
    template_name = "app_flight/airplane_tickets.html"
    form_class = UserFeedbackForm

    @property
    def context_data(self):
        if not hasattr(self, "_context_data"):
            self._context_data = self.get_context_data()
        return self._context_data

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ticket_id = self.kwargs.get("pk")
        ticket_obj = get_object_or_404(AirplaneTicket, id=ticket_id)
        context["ticket"] = ticket_obj

        traveler_adult, traveler_child, traveler_infant = self.get_traveler_numbers()
        total_adult_amount = ticket_obj.get_ticket_price_method(
            passenger_type="adult", traveler=traveler_adult
        )
        total_child_amount = ticket_obj.get_ticket_price_method(
            passenger_type="child", traveler=traveler_child
        )
        total_infant_amount = ticket_obj.get_ticket_price_method(
            passenger_type="infant", traveler=traveler_infant
        )

        total_amount = total_adult_amount + total_child_amount + total_infant_amount

        order_flight_forms = self._get_order_flight_forms(
            categories=["adult", "child", "infant"],
            extras=[traveler_adult, traveler_child, traveler_infant],
        )
        amount_infos = [
            {'type' : 'adult', 'count': traveler_adult,'amount':total_adult_amount},
            {'type' : 'child', 'count': traveler_child,'amount':total_child_amount},
            {'type' : 'infant', 'count': traveler_infant,'amount':total_infant_amount},
        ]
        context["order_flight_forms"] = order_flight_forms
        context["total_amount"] = total_amount
        context["amount_infos"] = amount_infos
        context["total_traveler"] = traveler_adult+traveler_child+traveler_infant

        return context

    def _get_order_flight_forms(self, categories, extras):
        order_forms = []
        for category, extra in zip(categories, extras):
            OrderFormSet = formset_factory(OrderFlightForm, extra=extra)
            order_forms.append(
                OrderFormSet(
                    data=self.request.POST or None,
                    prefix=category,
                    form_kwargs={"category": category},
                )
            )
        return order_forms

    def get_traveler_numbers(self):
        ticket_query_params = self.request.session.get("ticket_query_params", {})
        traveler_adult = int(ticket_query_params.get("traveler_adult", 1))
        traveler_child = int(ticket_query_params.get("traveler_child", 0))
        traveler_infant = int(ticket_query_params.get("traveler_infant", 0))
        return traveler_adult, traveler_child, traveler_infant

    def form_valid(self, order_flight_forms):
        form = self.get_form()
        order_obj = Order.objects.create(
            user=self.request.user.customuser,
            total_amount=self.get_context_data().get("total_amount"),
        )
        self.oder_id = order_obj.id
        for formset in order_flight_forms:
                for form in formset:
                    new_form = form.save(commit=False)
                    new_form.ticket = self.get_context_data().get("ticket")
                    new_form.order = order_obj
                    new_form.save()
        return super().form_valid(form)

    def form_invalid(self):
        return self.render_to_response(self.get_context_data())

    def post(self, request, *args, **kwargs):
        traveler_adult, traveler_child, traveler_infant = self.get_traveler_numbers()
        order_flight_forms = self._get_order_flight_forms(
            categories=["adult", "child", "infant"],
            extras=[traveler_adult, traveler_child, traveler_infant],
        )
        if all([formset.is_valid() for formset in order_flight_forms]):
            return self.form_valid(order_flight_forms)
        else:
            return self.form_invalid()

    def get_success_url(self):
        return reverse_lazy('app_flight:tickets_payments', kwargs={'pk': self.oder_id})


@method_decorator(signin_decorators, name="dispatch")
class AirPlaneTicketsPaymentsView(FormView):
    template_name = "app_flight/payment.html"
    form_class = FlightPaymentsForm
    success_url = reverse_lazy("app_main:order-list")

    def form_valid(self, form):
        payment = form.save(commit=False)

        # payment.save()
        messages.success(self.request, 'Payment has been completed successfully !')
        return super(AirPlaneTicketsPaymentsView, self).form_valid(form)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
