from django.db import models
from Users.models import CustomUser
from django.utils import timezone

class Crop(models.Model):
    name = models.CharField(max_length=100) # e.g., Maize, Wheat, Tomatoes
    variety = models.CharField(max_length=100) # e.g., Hybrid 614
    planting_date = models.DateField()
    expected_harvest_date = models.DateField()
    acreage = models.DecimalField(max_digits=5, decimal_places=2)
    # Keeping your original status for record, though 'stage' in Field will drive logic
    status = models.CharField(max_length=20, default='Growing') 

    def __str__(self):
        return f"{self.name} ({self.variety})"

class Field(models.Model):
    STAGE_CHOICES = [
        ('PLANTED', 'Planted'),
        ('GROWING', 'Growing'),
        ('READY', 'Ready'),
        ('HARVESTED', 'Harvested'),
    ]

    name = models.CharField(max_length=100) # e.g., Section A, North Wing
    
    # LINKING CROP TO FIELD
    crop = models.OneToOneField(Crop, on_delete=models.CASCADE, related_name='field_location')
    
    # Requirement #2: Assigning fields to agents
    agent = models.ForeignKey(
        CustomUser, 
        on_delete=models.SET_NULL, 
        null=True, 
        limit_choices_to={'user_type': '2'},
        related_name='assigned_fields'
    )
    
    # Requirement #3 & #4: Updates and Stages
    stage = models.CharField(max_length=20, choices=STAGE_CHOICES, default='PLANTED')
    notes = models.TextField(blank=True, help_text="Observations from the field agent")
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-last_updated']

    def __str__(self):
        return f"{self.name} - {self.crop.name}"

    # Requirement #5: Computed Status Logic
    @property
    def computed_status(self):
        """
        Logic:
        - Completed: Stage is Harvested.
        - At Risk: Current date is past Crop.expected_harvest_date OR > 90 days.
        - Active: Otherwise.
        """
        if self.stage == 'HARVESTED':
            return 'Completed'
        
        # Check against the expected date in the linked Crop model
        if timezone.now().date() > self.crop.expected_harvest_date:
            return 'At Risk'
            
        days_since_planting = (timezone.now().date() - self.crop.planting_date).days
        if days_since_planting > 90 and self.stage != 'READY':
            return 'At Risk'
            
        return 'Active'