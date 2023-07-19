from django.db import models
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

class TourPackageModel(models.Model):
    package_title = models.CharField(max_length=525, null=True)
    tour_location = models.ForeignKey(TourLocationModel, on_delete=models.CASCADE, null=True, blank=True)
    tour_duration = models.IntegerField(null=True, blank=True)
    peoples_limit = models.PositiveIntegerField(default=1, null=True, blank=True)

    details = RichTextUploadingField(null=True)
    options = RichTextUploadingField(null=True)
    policy = RichTextUploadingField(null=True)

    adult_traveler = models.PositiveIntegerField(null=True, default=1)
    child_traveler = models.PositiveIntegerField(null=True, blank=True)
    infant_traveler = models.PositiveIntegerField(null=True, blank=True)

    journey_date = models.DateTimeField()

    package_price = models.FloatField(null=True, blank=True)
    discount = models.ForeignKey("app_flight.DiscountModel", on_delete=models.CASCADE, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.id}- {self.package_title}"


    def get_discount_price(self):
        if self.discount:
            return (self.package_price / 100) * self.discount
            

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
        verbose_name_plural = "Tour Packages Images"

        ordering = [
            '-id'
        ]
