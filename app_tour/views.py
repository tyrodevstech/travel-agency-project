from django.shortcuts import get_object_or_404
from django.urls import reverse, reverse_lazy
from django.contrib import messages
from django.views.generic import ListView, FormView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from app_tour.filters import TourPackageFilters
from app_tour.models import TourPackageModel, TourPackageImages, TourOrderModel

from app_tour.forms import TourPackageOrderForm, TourPaymentsForm


signin_decorators = [login_required(login_url="app_main:signin")]

# Create your views here.
class TourIndexView(ListView):
    template_name = "app_tour/index.html"
    model = TourPackageModel
    context_object_name = 'tour_packages'
    def get_queryset(self):
        queryset = super().get_queryset()
        filter_data = self.request.GET.copy()
        self.filterset = TourPackageFilters(filter_data, queryset=queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter_form'] = self.filterset.form
        return context




@method_decorator(signin_decorators, name="dispatch")
class TourDetailsView(FormView):
    template_name = "app_tour/details.html"
    form_class = TourPackageOrderForm
    # success_url = reverse_lazy("app_main:home")
    order_id = None


    def form_valid(self, form):
        pk = self.kwargs.get('pk')
        get_hotel_name = self.request.POST.get('hotel_name', None)
        order = form.save(commit=False)
        order.user = self.request.user
        order.package = get_object_or_404(TourPackageModel, id=pk)
        order.hotel_name = get_hotel_name
        order.save()
        self.order_id = order.id
        return super(TourDetailsView, self).form_valid(form)

    def get_success_url(self):
         print(self.order_id)
         return reverse('app_tour:tour_payments', kwargs={'pk': self.order_id})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs.get('pk')
        context['tour_package'] = get_object_or_404(TourPackageModel, id=pk)
        context['sliders'] = TourPackageImages.objects.filter(package__id=pk)
        return context




@method_decorator(signin_decorators, name="dispatch")
class TourPaymentsView(FormView):
    template_name = 'app_tour/payments.html'
    form_class = TourPaymentsForm
    success_url = reverse_lazy("app_main:order-list")


    def form_valid(self, form):
        payment = form.save(commit=False)
        context = self.get_context_data()
        payment.order = context.get('order_obj')
        payment.adults_fare = context.get('adults_fare')
        payment.childrens_fare = context.get('childrens_fare')
        payment.infants_fare = context.get('infants_fare')
        payment.sub_total_fare = context.get('sub_total')
        payment.total_fare = context.get('total_fare')
        payment.total_traveler = context.get('total_traveler')
        payment.is_paid = True

        payment.save()
        messages.success(self.request, 'Payment has been completed successfully !')
        return super(TourPaymentsView, self).form_valid(form)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs.get('pk')
        order = get_object_or_404(TourOrderModel, id=pk)

        children_base_fare = order.package.package_price - ((order.package.package_price / 100) * order.package.Children_package_price)
        infant_base_fare = order.package.package_price - ((order.package.package_price / 100) * order.package.Infant_package_price)
        
        adults_fare = order.package.package_price * order.adult_traveler if order.adult_traveler else 0
        childrens_fare = children_base_fare * order.child_traveler if order.child_traveler else 0
        infants_fare = infant_base_fare * order.infant_traveler if order.infant_traveler else 0

        sub_total = adults_fare + childrens_fare + infants_fare
        total_fare = sub_total - order.package.get_discount_price() if order.package.discount else sub_total
        discount_price = order.package.get_discount_price()

        total_traveler = 0
        if order.child_traveler:
            if order.infant_traveler:
                total_traveler = order.adult_traveler + order.child_traveler + order.infant_traveler
            else:
                total_traveler = order.adult_traveler + order.child_traveler
        else:
            total_traveler = order.adult_traveler

        
        context['adults_fare'] = adults_fare
        context['childrens_fare'] = childrens_fare
        context['infants_fare'] = infants_fare
        context['sub_total'] = sub_total
        context['total_fare'] = total_fare
        context['discount_price'] = discount_price
        context['total_traveler'] = total_traveler
        context['order_obj'] = order
        return context