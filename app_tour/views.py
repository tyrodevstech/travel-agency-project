from django.shortcuts import get_object_or_404, render
from django.views.generic import ListView, TemplateView

# Create your views here.
class TourIndexView(TemplateView):
    template_name = "app_tour/index.html"
