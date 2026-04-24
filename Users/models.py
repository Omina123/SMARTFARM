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

# class Crop(models.Model):
#     name = models.CharField(max_length=100) # e.g., Maize, Wheat, Tomatoes
#     variety = models.CharField(max_length=100) # e.g., Hybrid 614
#     planting_date = models.DateField()
#     expected_harvest_date = models.DateField()
#     acreage = models.DecimalField(max_digits=5, decimal_places=2)
#     status = models.CharField(max_length=20, default='Growing') # Seedling, Growing, Harvested

#     def __str__(self):
#         return f"{self.name} ({self.variety})"