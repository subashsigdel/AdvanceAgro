from django.db import models
from datetime import timedelta

class CropTimeline(models.Model):
    CROP_TYPES = [
        ('प्याज', 'प्याज'),
        ('टमाटर', 'टमाटर'),
        ('धान', 'धान'),
        ('तोरी', 'तोरी'),
        ('फुल ', 'फुल '),
        
    ]

    crop_type = models.CharField(max_length=100, choices=CROP_TYPES, unique=True)
    ideal_starting_temperature = models.FloatField(null=True, blank=True)
    ideal_starting_moisture = models.FloatField(null=True, blank=True)
    field_name = models.CharField(max_length=255, null=True, blank=True)
    pesticide_time = models.DateTimeField()
    migration_time = models.DateTimeField(null=True, blank=True)
    harvesting_time = models.DateTimeField()
    initial_moisture = models.FloatField()
    initial_temperature = models.FloatField()
    harvesting_time = models.DateTimeField()
    created_date = models.DateTimeField(auto_now_add=True)
    edited_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.crop_type} Timeline"
    


class Crop(models.Model):
    name = models.CharField(max_length=255)
    pesticide_time = models.DateTimeField()
    migration_time = models.DateTimeField(null=True, blank=True)
    harvesting_time = models.DateTimeField()