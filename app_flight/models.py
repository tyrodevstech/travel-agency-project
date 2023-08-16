from django.db import models
from django.utils import timezone
from django_countries.fields import CountryField
from ckeditor_uploader.fields import RichTextUploadingField
from app_main.models import CustomUser


# Create your models here.
class Airport(models.Model):
    city = models.CharField(max_length=122, null=True)
    country = CountryField()
    name = models.CharField(max_length=122, null=True)
    code = models.CharField(max_length=3, null=True)

    def __str__(self):
        return f"{self.name} ({self.code})"

    class Meta:
        verbose_name = "Airport"
        verbose_name_plural = "Airports"
        ordering = ["-id"]


class Airplane(models.Model):
    name = models.CharField(max_length=122, null=True)
    model = models.CharField(max_length=122, null=True)
    logo = models.ImageField(upload_to="airplane_logo", null=True, blank=True)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = "Airplane"
        verbose_name_plural = "Airplanes"
        ordering = ["-id"]


class Discount(models.Model):
    name = models.CharField(max_length=122, null=True)
    code = models.CharField(max_length=122, null=True)
    amount = models.FloatField(null=True)
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.amount}% | {self.name}"

    class Meta:
        verbose_name = "Discount"
        verbose_name_plural = "Discounts"
        ordering = ["-id"]


class AirplaneTicket(models.Model):
    FLIGHT_TYPE_CHOICES = [
        ("Economy", "Economy"),
        ("Business", "Business"),
    ]
    airplane = models.ForeignKey(Airplane, on_delete=models.CASCADE, null=True)
    discount = models.ForeignKey(
        Discount, on_delete=models.CASCADE, null=True, blank=True
    )
    flight_type = models.CharField(
        max_length=122, choices=FLIGHT_TYPE_CHOICES, null=True, default="Economy"
    )

    duration = models.CharField(max_length=25, null=True, blank=True)

    base_price = models.FloatField(null=True, blank=True)

    child_discount = models.FloatField(null=True, blank=True)
    infant_discount = models.FloatField(null=True, blank=True)

    tax = models.FloatField(null=True, blank=True)

    baggage_cabin = models.FloatField(
        null=True, blank=True, verbose_name="Baggage KG (cabin)"
    )
    baggage_checkin = models.FloatField(
        null=True, blank=True, verbose_name="Baggage KG (check-in)"
    )

    location_from = models.ForeignKey(
        Airport, on_delete=models.CASCADE, null=True, related_name="location_from"
    )
    location_to = models.ForeignKey(
        Airport, on_delete=models.CASCADE, null=True, related_name="location_to"
    )

    depart_date = models.DateField(default=timezone.now)
    depart_time = models.TimeField(default=timezone.now)

    arrive_date = models.DateField(default=timezone.now)
    arrive_time = models.TimeField(default=timezone.now)

    policy = RichTextUploadingField(null=True, blank=True)

    def __str__(self):
        return f"Ticket {self.id} - {self.airplane.name} ({self.flight_type})"

    def get_total_baggage(self):
        if self.baggage_cabin and self.baggage_checkin:
            return self.baggage_cabin + self.baggage_checkin

    def total_adult_price(self):
        return self.base_adult_fare + self.adult_tax

    def get_ticket_discount_price(self,total):
        if self.discount:
            return (total / 100) * self.discount.amount
        else:
            return 0

    @property
    def get_ticket_price(self, passenger_type="adult", traveler=1):
        base_price = self.base_price * traveler
        if passenger_type == "child":
            base_price *= self.child_discount
        elif passenger_type == "infant":
            base_price *= self.infant_discount
        ticket_price = base_price + (base_price * self.tax / 100)
        return ticket_price

    def get_ticket_price_method(self, passenger_type="adult", traveler=1):
        ticket_price = 0
        if traveler > 0:
            base_price = self.base_price * traveler
            ticket_price = base_price + (base_price * self.tax / 100)
            if passenger_type == "child":
                ticket_price = ticket_price - (ticket_price * self.child_discount / 100)
            elif passenger_type == "infant":
                ticket_price = ticket_price - (
                    ticket_price * self.infant_discount / 100
                )
        return ticket_price

    class Meta:
        verbose_name = "Airplane Ticket"
        verbose_name_plural = "Airplane Tickets"
        ordering = ["-id"]


class Order(models.Model):
    STATUS_CHOICES = [
        ("PENDING", "Pending"),
        ("CONFIRMED", "Confirmed"),
        ("CANCELLED", "Cancelled"),
    ]

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="PENDING")
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Order {self.id} - {self.user} - {self.status}"


class Payment(models.Model):
    STATUS_CHOICES = [
        ("PENDING", "Pending"),
        ("COMPLETED", "Completed"),
        ("FAILED", "Failed"),
    ]

    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    payment_status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="PENDING"
    )
    payment_amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Payment for Order {self.order.id} - {self.payment_status}"


class OrderFlight(models.Model):
    TITLE_CHOICES = [
        ("MR.", "Mr."),
        ("MS.", "Ms."),
        ("MRS.", "Mrs."),
        ("MASTER.", "Master"),
        ("MISS.", "Miss"),
        ("INFANT.", "Infant"),
    ]

    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    title = models.CharField(max_length=10, choices=TITLE_CHOICES, default="MR.")
    ticket = models.ForeignKey(AirplaneTicket, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=122)
    last_name = models.CharField(max_length=122)
    email = models.EmailField(max_length=122)
    phone = models.CharField(max_length=20)
    date_of_birth = models.DateField(default=timezone.now)
    nationality = CountryField(default='BD')

    def __str__(self):
        return f"Order {self.order.id} - {self.first_name} {self.last_name}"

    class Meta:
        verbose_name = "Order Flight"
        verbose_name_plural = "Order Flights"
        ordering = ["-id"]
