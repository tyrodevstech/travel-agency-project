from django.contrib import admin
from app_main.models import CustomUser

# Register your models here.
admin.site.site_header = "Travel Agency"

admin.site.register(CustomUser)


