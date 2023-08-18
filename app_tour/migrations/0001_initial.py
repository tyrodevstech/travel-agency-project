
import ckeditor_uploader.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_countries.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('app_flight', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='HotelModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hotel_name', models.CharField(max_length=122, null=True, verbose_name='Name')),
                ('cover_image', models.ImageField(null=True, upload_to='tour_package_images', verbose_name='Cover Image')),
                ('link', models.URLField(blank=True, default='#', null=True, verbose_name='Hotel Link')),
            ],
            options={
                'verbose_name': 'Hotel',
                'verbose_name_plural': 'Hotels',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='TourLocationModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('country', django_countries.fields.CountryField(max_length=2)),
                ('district', models.CharField(max_length=122, null=True)),
                ('location_name', models.CharField(max_length=225, null=True, verbose_name='location name')),
                ('code', models.CharField(max_length=3, null=True)),
            ],
            options={
                'verbose_name': 'Tour Location',
                'verbose_name_plural': 'Tour Locations',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='TourOrderModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('adult_traveler', models.PositiveIntegerField(default=1, null=True)),
                ('child_traveler', models.PositiveIntegerField(blank=True, null=True)),
                ('infant_traveler', models.PositiveIntegerField(blank=True, null=True)),
                ('hotel_name', models.CharField(max_length=525, null=True)),
                ('journey_date', models.DateTimeField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Tour Package Order',
                'verbose_name_plural': 'Tour Package Orders',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='TourPaymentsModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_card_name', models.CharField(max_length=125, null=True)),
                ('user_card_number', models.CharField(max_length=125, null=True)),
                ('user_cvc_number', models.CharField(max_length=125, null=True)),
                ('user_postal_code', models.CharField(max_length=125, null=True)),
                ('adults_fare', models.FloatField(null=True)),
                ('childrens_fare', models.FloatField(blank=True, null=True)),
                ('infants_fare', models.FloatField(blank=True, null=True)),
                ('total_traveler', models.PositiveIntegerField(blank=True, null=True)),
                ('sub_total_fare', models.FloatField(null=True)),
                ('total_fare', models.FloatField(null=True)),
                ('is_paid', models.BooleanField(default=False, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('order', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='app_tour.tourordermodel')),
            ],
            options={
                'verbose_name': 'Tour Package Payment',
                'verbose_name_plural': 'Tour Package Payments',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='TourPackageModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('package_title', models.CharField(max_length=525, null=True)),
                ('package_cover_image', models.ImageField(blank=True, null=True, upload_to='tour_package_cover_images')),
                ('tour_duration', models.IntegerField(blank=True, null=True)),
                ('peoples_limit', models.PositiveIntegerField(blank=True, default=1, null=True)),
                ('details', ckeditor_uploader.fields.RichTextUploadingField(null=True)),
                ('options', ckeditor_uploader.fields.RichTextUploadingField(null=True)),
                ('policy', ckeditor_uploader.fields.RichTextUploadingField(null=True)),
                ('journey_date', models.DateTimeField()),
                ('package_price', models.FloatField(blank=True, null=True)),
                ('Children_package_price', models.FloatField(default=50, help_text='Enter 50 percent children traveler', null=True)),
                ('Infant_package_price', models.FloatField(default=90, help_text='Enter 90 percent infant traveler', null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('discount', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app_flight.discount')),
                ('hotel', models.ManyToManyField(to='app_tour.hotelmodel')),
                ('tour_location', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app_tour.tourlocationmodel')),
            ],
            options={
                'verbose_name': 'Tour Package',
                'verbose_name_plural': 'Tour Packages',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='TourPackageImages',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image_title', models.CharField(max_length=122, null=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='tour_package_images')),
                ('package', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app_tour.tourpackagemodel')),
            ],
            options={
                'verbose_name': 'Tour Package Image',
                'verbose_name_plural': 'Tour Package Images',
                'ordering': ['-id'],
            },
        ),
        migrations.AddField(
            model_name='tourordermodel',
            name='package',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app_tour.tourpackagemodel'),
        ),
        migrations.AddField(
            model_name='tourordermodel',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]