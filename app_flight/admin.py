from django.contrib import admin
from app_flight.models import *

# Register your models here.

admin.site.register(AirportModel)
admin.site.register(AirplaneModel)
admin.site.register(DiscountModel)
admin.site.register(AirPlaneTicketModel)
admin.site.register(OrderFlightModel)
