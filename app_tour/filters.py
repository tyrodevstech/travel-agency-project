import django_filters as filter
from django import forms
from django_filters.widgets import RangeWidget
from django_property_filter import PropertyFilterSet, PropertyRangeFilter

from app_tour.models import TourLocationModel, TourPackageModel


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

class TourPackageFilters(PropertyFilterSet):
    price = PropertyRangeFilter(
        field_name='get_discount_price',
        label="Price",
        widget=CustomRangeWidget
    )
    tour_location = filter.ModelChoiceFilter(queryset=TourLocationModel.objects.all(), empty_label='Select Location / Tour')
    package_title = filter.CharFilter(widget=forms.TextInput(attrs={'placeholder':'Search by title...'}))
    journey_date = filter.DateFilter(field_name='journey_date',widget=forms.DateInput(attrs={'type':'date'}))

    class Meta:
        model = TourPackageModel
        fields = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.filters["airplane"].field.label_from_instance = lambda location: location.location_name
