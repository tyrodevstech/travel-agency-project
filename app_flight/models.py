from django.db import models
from django.utils import timezone
from django_countries.fields import CountryField

# Create your models here.
class AirportModel(models.Model):
    city = models.CharField(max_length=122, null=True)
    country = CountryField()
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

class AirplaneModel(models.Model):
    airplane_name = models.CharField(max_length=122, null=True)
    airplane_model = models.CharField(max_length=122, null=True)
    airplane_logo = models.ImageField(upload_to="airplane_logo", null=True, blank=True)

    def __str__(self):
        return f"{self.id}- {self.airplane_name}"
    
    class Meta:
        verbose_name = "Airplane"
        verbose_name_plural = "Airplanes"

        ordering = [
            '-id'
        ]


class DiscountModel(models.Model):
    discount_name = models.CharField(max_length=122, null=True)
    discount_code = models.CharField(max_length=122, null=True)
    amount = models.FloatField(null=True)
    start_date = models.DateTimeField(auto_now=True)
    end_date = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.amount}% | {self.discount_name}"

    class Meta:
        verbose_name = "Discount"
        verbose_name_plural = "Discounts"

        ordering = [
            '-id'
        ]


class AirPlaneTicketModel(models.Model):
    FLGHT_TYPE_CHOICES = (
        ('Economy', 'Economy'),
        ('Business', 'Business'),
    )

    airplane = models.ForeignKey(AirplaneModel, on_delete=models.CASCADE, null=True)
    discount = models.ForeignKey(DiscountModel, on_delete=models.CASCADE, null=True, blank=True)
    flight_type =  models.CharField(max_length=122, choices=FLGHT_TYPE_CHOICES, null=True, default='Economy')
    
    duration = models.CharField(max_length=25, null=True, blank=True)
    
    base_price = models.FloatField(null=True, blank=True)

    child_discount = models.FloatField(null=True, blank=True)
    infant_discount = models.FloatField(null=True, blank=True)

    tax = models.FloatField(null=True, blank=True)
    
    baggage_cabin = models.FloatField(null=True, blank=True, verbose_name="Baggage KG (cabin)")
    baggage_checkin = models.FloatField(null=True, blank=True, verbose_name="Baggage KG (check-in)")

    location_from = models.ForeignKey(AirportModel, on_delete=models.CASCADE, null=True, related_name="location_from")
    location_to = models.ForeignKey(AirportModel, on_delete=models.CASCADE, null=True, related_name="location_to")

    depart_date = models.DateField(default= timezone.now)
    depart_time = models.TimeField(default= timezone.now)

    arrive_date = models.DateField(default= timezone.now)
    arrive_time = models.TimeField(default= timezone.now)

    def __str__(self):
        return f"{self.id}- {self.airplane.airplane_name} ({self.flight_type})"


    def get_total_baggage(self):
        if self.baggage_cabin and self.baggage_checkin:
            return self.baggage_cabin + self.baggage_checkin
    
    def total_adult_price(self):
        return self.base_adult_fare + self.adult_tax
    
    def get_ticket_price(self,passenger_type='adult'):
        base_price = self.base_price  # Base price for the ticket
        if passenger_type == 'child':
            base_price *= self.child_discount  # Apply a 25% discount for child passengers
        elif passenger_type == 'infant':
            base_price *= self.infant_discount  # Apply a 50% discount for infant passengers

        ticket_price = base_price + (base_price * self.tax)

        return ticket_price

    class Meta:
        verbose_name = "AirPlane Ticket"
        verbose_name_plural = "AirPlane Tickets"

        ordering = [
            '-id'
        ]


class OrderFlightModel(models.Model):
    SELECT_TITLE = (
        ('MR.', 'MR.'),
        ('MS.', 'MS.'),
        ('MRS.', 'MRS.'),
        ('MASTER..', 'MASTER.'),
        ('MISS.', 'MISS.'),
    )

    select_title =  models.CharField(max_length=122, choices=SELECT_TITLE, null=True, default='MR.')
    ticket = models.ForeignKey(AirPlaneTicketModel, on_delete=models.CASCADE, null=True)
    first_name = models.CharField(max_length=122, null=True)
    last_name = models.CharField(max_length=122, null=True)
    email = models.CharField(max_length=122, null=True)
    phone = models.CharField(max_length=122, null=True)
    date_of_birth = models.DateField(auto_now=True, null=True)
    nationality = CountryField()

    def __str__(self):
        return f"{self.id}- {self.first_name} ({self.last_name}) - {self.phone}"

    class Meta:
        verbose_name = "Order Flight"
        verbose_name_plural = "Order Flights"

        ordering = [
            '-id'
        ]
