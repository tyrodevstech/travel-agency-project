from django.contrib import admin
from app_main.models import CustomUser, UserFeedback

# Register your models here.
admin.site.site_header = "Travel Agency"

class UserFeedbackModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'phone',)
    search_fields = ['name', 'phone']


admin.site.register(UserFeedback, UserFeedbackModelAdmin)
admin.site.register(CustomUser)


