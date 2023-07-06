from django_filters import CharFilter

class DayNightFilter(CharFilter):
    def filter(self, qs, value):
        if value == 'day':
            return qs.filter(start_date__gte='06:00:00', start_date__lt='18:00:00')
        elif value == 'night':
            return qs.exclude(start_date__gte='06:00:00', start_date__lt='18:00:00')
        else:
            return qs