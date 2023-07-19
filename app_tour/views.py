from django.shortcuts import get_object_or_404, render
from django.views.generic import ListView, TemplateView
from app_tour.filters import TourPackageFilters
from app_tour.models import TourPackageModel
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


class TourDetailsView(TemplateView):
    template_name = "app_tour/details.html"
