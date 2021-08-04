from django.db import models
import random
import string

def generate_license():
    keyset = string.ascii_uppercase + string.digits
    keysetpart = lambda : "".join(random.choices(keyset, k=3))
    return "-".join([keysetpart() for _ in range(4)])

# Create your models here.
class LicenseKey(models.Model):
    key = models.CharField(max_length=15, default=generate_license, editable=False, primary_key=True)
    hardware_id = models.CharField(max_length=200, blank=True)
    name = models.CharField(max_length=255)
    email = models.EmailField(null=True, blank=True)
    last_activity = models.DateTimeField(blank=True, null=True)
    active = models.BooleanField(default=True) #If the license key is active or has expired
