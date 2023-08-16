from django.contrib import admin
from app_tour.models import *

# Register your models here.

admin.site.register(TourLocationModel)
admin.site.register(TourPackageModel)
admin.site.register(TourPackageImages)
admin.site.register(TourOrderModel)


class TourPaymentsModelAdmin(admin.ModelAdmin):
    list_display = ('get_username', 'user_card_name', 'get_order_id', 'get_package_title', 'total_traveler', 'total_fare',)
    search_fields = ['user_card_name', 'created_at', 'user_card_number',]
    list_filter = ('is_paid',)

    @admin.display(ordering='order__id', description='Order ID')
    def get_order_id(self, obj):
        return obj.order.id

    @admin.display(ordering='order.package__package_title', description='Order Name')
    def get_package_title(self, obj):
        return obj.order.package.package_title

    @admin.display(ordering='order.user__username', description='Username')
    def get_username(self, obj):
        return obj.order.user.username


admin.site.register(TourPaymentsModel, TourPaymentsModelAdmin)
admin.site.register(HotelModel)
