from django.db import models

# Create your models here.
class TourLocationModel(models.Model):
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
    package_title = models.CharField(max_length=225, null=True)
    overview = models.TextField(max_length=755, null=True)
    duration = models.IntegerField(null=True, blank=True)
    requirements = models.TextField(max_length=755, null=True)
    location = models.CharField(max_length=122, null=True)
    timing = models.CharField(max_length=122, null=True)
    description = models.TextField(max_length=755, null=True)
    additional_information = models.TextField(max_length=755, null=True)
    travel_tips = models.TextField(max_length=755, null=True)
    policy = models.TextField(max_length=755, null=True)

    adult_traveler = models.IntegerField(null=True, default=1)
    child_traveler = models.IntegerField(null=True, blank=True)
    infant_traveler = models.IntegerField(null=True, blank=True)

    journey_date = models.DateTimeField()
    package_price = models.FloatField(null=True, blank=True)

    discount = models.ForeignKey("app_flight.DiscountModel", on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.id}- {self.package_title}"

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
