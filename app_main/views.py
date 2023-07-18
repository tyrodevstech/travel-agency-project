from django.shortcuts import render
from app_flight.filters import AirPlaneTicketFilters
from app_flight.models import AirPlaneTicketModel

# Create your views here.


def index_view(request):
    context = {
        'filter':AirPlaneTicketFilters(request.GET, queryset=AirPlaneTicketModel.objects.all())
    }
    return render(request, 'app_main/index.html',context)