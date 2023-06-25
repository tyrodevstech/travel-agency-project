from django.db import models

# Create your models here.
class AirportModel(models.Model):
    city = models.CharField(max_length=122, null=True)
    country = models.CharField(max_length=122, null=True)
    airport = models.CharField(max_length=122, null=True)
    code = models.CharField(max_length=3, null=True)

    def __str__(self):
        return f"{self.id}- {self.code}"

    class Meta:
        verbose_name = "Airport"
        verbose_name_plural = "Airports"

        ordering = [
            '-id'
        ]
