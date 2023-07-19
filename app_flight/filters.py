import django_filters as filter
from django_filters.widgets import RangeWidget
from django_property_filter import PropertyRangeFilter,PropertyFilterSet
from django import forms

from app_flight.models import AirplaneModel, AirPlaneTicketModel, AirportModel
class CustomRangeWidget(RangeWidget):
    template_name = 'app_flight/widgets/rangeinput.html'

class CustomCheckboxSelectMultiple(forms.CheckboxSelectMultiple):
    template_name = 'app_flight/widgets/custom_checkbox.html'

class DayNightFilter(filter.MultipleChoiceFilter):
    def filter(self, qs, value):
        if "day" in value and "night" in value:
            return qs
        elif "day" in value:
            return qs.filter(depart_time__gte="06:00:00", depart_time__lt="18:00:00")
        elif "night" in value:
            return qs.exclude(depart_time__gte="06:00:00", depart_time__lt="18:00:00")
        return qs

class AirPlaneTicketFilters(PropertyFilterSet):
    airplane = filter.ModelMultipleChoiceFilter(
        queryset=AirplaneModel.objects.all(),
        widget=CustomCheckboxSelectMultiple
    )
    schedule = DayNightFilter(
        field_name="depart_time",
        lookup_expr="exact",
        choices=(('day', 'day'), ('night', 'night'))
    )
    ticket_price = PropertyRangeFilter(
        field_name='get_ticket_price',
        label="Price",
        widget=CustomRangeWidget
    )
    flight_type = filter.MultipleChoiceFilter(
        field_name='flight_type',
        choices=AirPlaneTicketModel.FLGHT_TYPE_CHOICES,
        widget=CustomCheckboxSelectMultiple
    )
    location_from = filter.ModelChoiceFilter(queryset=AirportModel.objects.all(), empty_label='Locaton From')
    location_to = filter.ModelChoiceFilter(queryset=AirportModel.objects.all(), empty_label='Locaton To')
    depart_date = filter.DateFilter(field_name='depart_date')

    class Meta:
        model = AirPlaneTicketModel
        fields = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.filters["airplane"].field.label_from_instance = lambda airplane: airplane.airplane_name
        self.filters["location_from"].field.label_from_instance = lambda airport: f"{airport.airport}, {airport.city}, {airport.country.name}"
        self.filters["location_to"].field.label_from_instance = lambda airport: f"{airport.airport}, {airport.city}, {airport.country.name}"
