from django.contrib import admin
from app_flight.models import *

# Register your models here.

admin.site.register(Airport)
admin.site.register(Airplane)
admin.site.register(Discount)
admin.site.register(AirplaneTicket)
admin.site.register(Order)
admin.site.register(OrderFlight)
admin.site.register(Payment)
