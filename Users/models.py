from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    # Updated roles to match SmartSeason Requirements
    USER_ROLES = (
        ('1', 'Admin'),
        ('2', 'Field Agent'),
    )
    user_type = models.CharField(max_length=1, choices=USER_ROLES, default='2')
    phone_number = models.CharField(max_length=15, blank=True)
    farm_name = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"{self.username} ({self.get_user_type_display()})"

