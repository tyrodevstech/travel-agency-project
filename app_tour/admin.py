from django.contrib import admin
from app_tour.models import *

# Register your models here.

class TourLocationModelAdmin(admin.ModelAdmin):
    list_display = ('location_name', 'code', 'district', 'country',)
    search_fields = ['location_name', 'code',]

admin.site.register(TourLocationModel, TourLocationModelAdmin)

class TourLocationModelAdmin(admin.ModelAdmin):
    list_display = ('package_title', 'package_price', 'get_tour_location', 'get_discount',)
    search_fields = ['package_title', 'package_price',]

    @admin.display(ordering='location_name__id', description='Location')
    def get_tour_location(self, obj):
        return obj.tour_location.location_name

    def get_discount(self, obj):
        if obj.discount:
            return f"{obj.discount.amount}%"
        else:
            return "N/A"
        

admin.site.register(TourPackageModel, TourLocationModelAdmin)


class TourPackageImagesAdmin(admin.ModelAdmin):
    list_display = ('get_package', 'image_title',)
    search_fields = ['image_title',]

    @admin.display(ordering='package__id', description='Package Name')
    def get_package(self, obj):
        return obj.package.package_title

admin.site.register(TourPackageImages, TourPackageImagesAdmin)


class TourOrderModelAdmin(admin.ModelAdmin):
    list_display = ('get_username', 'get_package', 'id', 'created_at')

    @admin.display(ordering='user__id', description='Username')
    def get_username(self, obj):
        return obj.user.username

    @admin.display(ordering='package__id', description='Package Name')
    def get_package(self, obj):
        return obj.package.package_title

admin.site.register(TourOrderModel, TourOrderModelAdmin)


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


class HotelModelAdmin(admin.ModelAdmin):
    list_display = ('hotel_name', 'link',)
    search_fields = ['hotel_name',]

admin.site.register(HotelModel, HotelModelAdmin)
