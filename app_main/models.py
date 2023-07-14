from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class CustomUser(models.Model):
    person = (
        ('','Select Gender'),
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other')
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=122, null=True)
    email = models.CharField(max_length=122, null=True)
    phone = models.CharField(max_length=122, null=True)
    gender = models.CharField(max_length=122, choices = person, null=True, blank=True)
    dob = models.DateField(null=True, blank=True)
    city = models.CharField(max_length=122, null=True, blank=True)
    country = models.CharField(max_length=122, null=True, blank=True)

    def __str__(self):
        return f"{self.id}- {self.name}"

    class Meta:
        verbose_name = "Custom User"
        verbose_name_plural = "Custom Users"

        ordering = [
            '-id'
        ]


class UserFeedback(models.Model):
    name = models.CharField(max_length=122, null=True)
    phone = models.CharField(max_length=122, null=True)
    message = models.TextField(max_length=900, null=True, blank=True)
    created_at = models.DateField(auto_now_add=True)


    def __str__(self):
        return f"{self.id}- {self.name}"

    class Meta:
        verbose_name = "User Feedback"
        verbose_name_plural = "User Feedbacks"

        ordering = [
            '-id'
        ]