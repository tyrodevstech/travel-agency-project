import django_filters

from app_flight.models import AirPlaneTicketModel
from app_flight.utils import DayNightFilter


class AirPlaneTicketFilters(django_filters.FilterSet):
    airplane_name = django_filters.CharFilter(field_name='airplane__airplane_name', lookup_expr='icontains')
    day_night = DayNightFilter(field_name='start_date', lookup_expr='exact')
    

    class Meta:
        model = AirPlaneTicketModel
        fields = {
            'flight_type': ['icontains'],
            }