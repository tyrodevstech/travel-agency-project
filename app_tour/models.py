from django.db import models
from django.contrib.auth.models import User
from django_countries.fields import CountryField
from ckeditor_uploader.fields import RichTextUploadingField

# Create your models here.
class TourLocationModel(models.Model):
    country = CountryField()
    district = models.CharField(max_length=122, null=True)
    location_name = models.CharField(max_length=225, null=True, verbose_name="location name")
    code = models.CharField(max_length=3, null=True)

    def __str__(self):
        return f"{self.id}- {self.location_name}"

    class Meta:
        verbose_name = "Tour Location"
        verbose_name_plural = "Tour Locations"

        ordering = [
            '-id'
        ]



class HotelModel(models.Model):
    hotel_name = models.CharField(max_length=122, null=True, verbose_name="Name")
    cover_image = models.ImageField(upload_to="tour_package_images", null=True, verbose_name="Cover Image")
    link = models.URLField(null=True, blank=True, default="#", verbose_name="Hotel Link")

    class Meta:
        verbose_name = "Hotel"
        verbose_name_plural = "Hotels"

        ordering = [
            '-id'
        ]

    def __str__(self):
        return f"{self.id}- {self.hotel_name}"



class TourPackageModel(models.Model):
    package_title = models.CharField(max_length=525, null=True)
    package_cover_image = models.ImageField(upload_to="tour_package_cover_images", null=True, blank=True)
    tour_location = models.ForeignKey(TourLocationModel, on_delete=models.CASCADE, null=True, blank=True)
    tour_duration = models.IntegerField(null=True, blank=True)
    peoples_limit = models.PositiveIntegerField(default=1, null=True, blank=True)

    details = RichTextUploadingField(null=True)
    options = RichTextUploadingField(null=True)
    policy = RichTextUploadingField(null=True)

    journey_date = models.DateTimeField()

    package_price = models.FloatField(null=True, blank=True)
    Children_package_price = models.FloatField(null=True, default= 50, help_text="Enter 50 percent children traveler")
    Infant_package_price = models.FloatField(null=True, default= 90, help_text="Enter 90 percent infant traveler")
    discount = models.ForeignKey("app_flight.DiscountModel", on_delete=models.CASCADE, null=True, blank=True)

    hotel = models.ManyToManyField(HotelModel)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.id}- {self.package_title}"


    def get_discount_price(self):
        if self.discount:
            return (self.package_price / 100) * self.discount.amount
            

    class Meta:
        verbose_name = "Tour Package"
        verbose_name_plural = "Tour Packages"

        ordering = [
            '-id'
        ]


class TourPackageImages(models.Model):
    package = models.ForeignKey(TourPackageModel, on_delete=models.CASCADE, null=True)
    image_title = models.CharField(max_length=122, null=True)
    image = models.ImageField(upload_to="tour_package_images", null=True, blank=True)

    def __str__(self):
        return f"{self.id}- {self.image_title}"

    class Meta:
        verbose_name = "Tour Package Image"
        verbose_name_plural = "Tour Package Images"

        ordering = [
            '-id'
        ]


class TourOrderModel(models.Model):
    user =  models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    package = models.ForeignKey(TourPackageModel, on_delete=models.CASCADE, null=True)
    
    adult_traveler = models.PositiveIntegerField(null=True, default=1)
    child_traveler = models.PositiveIntegerField(null=True, blank=True)
    infant_traveler = models.PositiveIntegerField(null=True, blank=True)
    hotel_name = models.CharField(max_length=525, null=True)
    journey_date = models.DateTimeField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order: {self.id}- {self.user.username}"

    class Meta:
        verbose_name = "Tour Package Order"
        verbose_name_plural = "Tour Package Orders"

        ordering = [
            '-id'
        ]


class TourPaymentsModel(models.Model):
    order = models.OneToOneField(TourOrderModel, on_delete=models.CASCADE, null=True)

    user_card_name = models.CharField(max_length=125, null=True)
    user_card_number = models.CharField(max_length=125, null=True)
    user_cvc_number = models.CharField(max_length=125, null=True)
    user_postal_code = models.CharField(max_length=125, null=True)

    adults_fare = models.FloatField(null=True)
    childrens_fare = models.FloatField(null=True, blank=True)
    infants_fare = models.FloatField(null=True, blank=True)

    total_traveler = models.PositiveIntegerField(null=True, blank=True)

    sub_total_fare = models.FloatField(null=True)
    total_fare = models.FloatField(null=True)

    is_paid = models.BooleanField(default=False, null=True)

    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"{self.id}- {self.user_card_name} | amount( {self.total_fare} )"

    class Meta:
        verbose_name = "Tour Package Payment"
        verbose_name_plural = "Tour Package Payments"

        ordering = [
            '-id'
        ]