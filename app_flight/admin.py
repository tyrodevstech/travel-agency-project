from django.contrib import admin
from app_flight.models import *

# Register your models here.

class AirportAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'city', 'country',)
    search_fields = ['name', 'code',]

admin.site.register(Airport, AirportAdmin)


class AirplaneAdmin(admin.ModelAdmin):
    list_display = ('name', 'model',)
    search_fields = ['name', 'model',]

admin.site.register(Airplane, AirplaneAdmin)


class DiscountAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'get_discount', 'created_at',)
    search_fields = ['name', 'code', 'amount',]

    def get_discount(self, obj):
        return f"{obj.amount}%"
        
admin.site.register(Discount, DiscountAdmin)


class AirplaneTicketAdmin(admin.ModelAdmin):
    list_display = ('get_ticket_name', 'flight_type', 'base_price', 'tax', 'get_discount',)
    list_filter = ('flight_type',)

    def get_ticket_name(self, obj):
        return f"{obj.airplane.name} ({obj.location_from.code}-{obj.location_to.code})"

    def get_discount(self, obj):
        if obj.discount:
            return f"{obj.discount.amount}%"
        else:
            return "N/A"

admin.site.register(AirplaneTicket, AirplaneTicketAdmin)


class OrderAdmin(admin.ModelAdmin):
    list_display = ('get_username', 'get_flight', 'total_amount', 'created_at',)
    search_fields = ['id', 'total_amount',]

    @admin.display(ordering='user__id', description='Username')
    def get_username(self, obj):
        return obj.user.name

    @admin.display(ordering='ticket__id', description='Flight')
    def get_flight(self, obj):
        if obj.ticket:
            return f"{obj.ticket.airplane.name} ({obj.ticket.location_from.code}-{obj.ticket.location_to.code})"
        else:
            return "N/A"

admin.site.register(Order, OrderAdmin)



class OrderFlightAdmin(admin.ModelAdmin):
    list_display = ('get_user_full_name', 'get_flight', 'get_order_id', 'email', 'phone',)
    search_fields = ['id', 'email', 'phone',]

    @admin.display(ordering='id', description='Username')
    def get_user_full_name(self, obj):
        return f"{obj.title} {obj.first_name} {obj.last_name}"

    @admin.display(ordering='order__id', description='Order ID')
    def get_order_id(self, obj):
        return obj.order.id

    @admin.display(ordering='ticket__id', description='Flight')
    def get_flight(self, obj):
        if obj.ticket:
            return f"{obj.ticket.airplane.name} ({obj.ticket.location_from.code}-{obj.ticket.location_to.code})"
        else:
            return "N/A"

admin.site.register(OrderFlight, OrderFlightAdmin)


class PaymentAdmin(admin.ModelAdmin):
    list_display = ('get_username', 'user_card_number', 'get_order_id', 'get_flight_name', 'total_traveler', 'total_fare', 'created_at',)
    search_fields = ['user_card_name', 'user_card_number', 'created_at',]
    list_filter = ('is_paid',)


    @admin.display(ordering='order.user__id', description='Username')
    def get_username(self, obj):
        return obj.order.user.name

    @admin.display(ordering='order__id', description='Order ID')
    def get_order_id(self, obj):
        return obj.order.id

    @admin.display(ordering='order.ticket__id', description='Flight')
    def get_flight_name(self, obj):
        return f"{obj.order.ticket.airplane.name} ({obj.order.ticket.location_from.code}-{obj.order.ticket.location_to.code})"

admin.site.register(Payment, PaymentAdmin)
