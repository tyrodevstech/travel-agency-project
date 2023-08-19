from django.contrib import admin
from app_main.models import CustomUser, UserFeedback

# Register your models here.
admin.site.site_header = "Travel Agency"

class UserFeedbackModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'phone',)
    search_fields = ['name', 'phone']

admin.site.register(UserFeedback, UserFeedbackModelAdmin)

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('name', 'get_username', 'email', 'phone')
    search_fields = ['name', 'phone', 'email',]

    @admin.display(ordering='user__id', description='username')
    def get_username(self, obj):
        return obj.user.username

admin.site.register(CustomUser, CustomUserAdmin)


