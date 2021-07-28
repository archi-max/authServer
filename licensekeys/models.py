from django.db import models

# Create your models here.
class LicenseKey(models.Model):
    key = models.CharField(max_length=15, unique=True)
    hardware_id = models.CharField(max_length=200, blank=True)
    name = models.CharField(max_length=255)
    email = models.EmailField(primary_key=True)
    last_activity = models.DateTimeField(blank=True)
    active = models.BooleanField(default=True)
