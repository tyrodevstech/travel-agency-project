# Generated by Django 4.2.2 on 2023-08-17 05:17

import ckeditor_uploader.fields
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import django_countries.fields


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("app_main", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Airplane",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=122, null=True)),
                ("model", models.CharField(max_length=122, null=True)),
                (
                    "logo",
                    models.ImageField(blank=True, null=True, upload_to="airplane_logo"),
                ),
            ],
            options={
                "verbose_name": "Airplane",
                "verbose_name_plural": "Airplanes",
                "ordering": ["-id"],
            },
        ),
        migrations.CreateModel(
            name="AirplaneTicket",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "flight_type",
                    models.CharField(
                        choices=[("Economy", "Economy"), ("Business", "Business")],
                        default="Economy",
                        max_length=122,
                        null=True,
                    ),
                ),
                ("duration", models.CharField(blank=True, max_length=25, null=True)),
                ("base_price", models.FloatField(blank=True, null=True)),
                ("child_discount", models.FloatField(blank=True, null=True)),
                ("infant_discount", models.FloatField(blank=True, null=True)),
                ("tax", models.FloatField(blank=True, null=True)),
                (
                    "baggage_cabin",
                    models.FloatField(
                        blank=True, null=True, verbose_name="Baggage KG (cabin)"
                    ),
                ),
                (
                    "baggage_checkin",
                    models.FloatField(
                        blank=True, null=True, verbose_name="Baggage KG (check-in)"
                    ),
                ),
                ("depart_date", models.DateField(default=django.utils.timezone.now)),
                ("depart_time", models.TimeField(default=django.utils.timezone.now)),
                ("arrive_date", models.DateField(default=django.utils.timezone.now)),
                ("arrive_time", models.TimeField(default=django.utils.timezone.now)),
                (
                    "policy",
                    ckeditor_uploader.fields.RichTextUploadingField(
                        blank=True, null=True
                    ),
                ),
                (
                    "airplane",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="app_flight.airplane",
                    ),
                ),
            ],
            options={
                "verbose_name": "Airplane Ticket",
                "verbose_name_plural": "Airplane Tickets",
                "ordering": ["-id"],
            },
        ),
        migrations.CreateModel(
            name="Airport",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("city", models.CharField(max_length=122, null=True)),
                ("country", django_countries.fields.CountryField(max_length=2)),
                ("name", models.CharField(max_length=122, null=True)),
                ("code", models.CharField(max_length=3, null=True)),
            ],
            options={
                "verbose_name": "Airport",
                "verbose_name_plural": "Airports",
                "ordering": ["-id"],
            },
        ),
        migrations.CreateModel(
            name="Discount",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=122, null=True)),
                ("code", models.CharField(max_length=122, null=True)),
                ("amount", models.FloatField(null=True)),
                ("start_date", models.DateTimeField(default=django.utils.timezone.now)),
                ("end_date", models.DateTimeField(default=django.utils.timezone.now)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
            options={
                "verbose_name": "Discount",
                "verbose_name_plural": "Discounts",
                "ordering": ["-id"],
            },
        ),
        migrations.CreateModel(
            name="Order",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("PENDING", "Pending"),
                            ("CONFIRMED", "Confirmed"),
                            ("CANCELLED", "Cancelled"),
                        ],
                        default="PENDING",
                        max_length=20,
                    ),
                ),
                ("total_amount", models.DecimalField(decimal_places=2, max_digits=10)),
                ("created_at", models.DateTimeField(default=django.utils.timezone.now)),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="app_main.customuser",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Payment",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "payment_status",
                    models.CharField(
                        choices=[
                            ("PENDING", "Pending"),
                            ("COMPLETED", "Completed"),
                            ("FAILED", "Failed"),
                        ],
                        default="PENDING",
                        max_length=20,
                    ),
                ),
                (
                    "payment_amount",
                    models.DecimalField(decimal_places=2, max_digits=10),
                ),
                ("payment_date", models.DateTimeField(blank=True, null=True)),
                (
                    "order",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="app_flight.order",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="OrderFlight",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "title",
                    models.CharField(
                        choices=[
                            ("MR.", "Mr."),
                            ("MS.", "Ms."),
                            ("MRS.", "Mrs."),
                            ("MASTER.", "Master"),
                            ("MISS.", "Miss"),
                            ("INFANT.", "Infant"),
                        ],
                        default="MR.",
                        max_length=10,
                    ),
                ),
                ("first_name", models.CharField(max_length=122)),
                ("last_name", models.CharField(max_length=122)),
                ("email", models.EmailField(max_length=122)),
                ("phone", models.CharField(max_length=20)),
                ("date_of_birth", models.DateField(default=django.utils.timezone.now)),
                (
                    "nationality",
                    django_countries.fields.CountryField(default="BD", max_length=2),
                ),
                (
                    "order",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="app_flight.order",
                    ),
                ),
                (
                    "ticket",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="app_flight.airplaneticket",
                    ),
                ),
            ],
            options={
                "verbose_name": "Order Flight",
                "verbose_name_plural": "Order Flights",
                "ordering": ["-id"],
            },
        ),
        migrations.AddField(
            model_name="airplaneticket",
            name="discount",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="app_flight.discount",
            ),
        ),
        migrations.AddField(
            model_name="airplaneticket",
            name="location_from",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="location_from",
                to="app_flight.airport",
            ),
        ),
        migrations.AddField(
            model_name="airplaneticket",
            name="location_to",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="location_to",
                to="app_flight.airport",
            ),
        ),
    ]
