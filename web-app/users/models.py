
# users/models.py
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, null=False, blank=False)
    # email = models.EmailField(unique=True, null=False, blank=False)
    is_driver = models.BooleanField(default=False)
    address = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)

    def __str__(self):
        return f'{self.name} Profile'

class DriverProfile(models.Model):

    VECHILE_TYPE = (
        ('SUV', 'SUV'),
        ('SEDAN', 'SEDAN'),
        ('Hybrid', 'Hybrid'),
        ('VAN', 'VAN'),
        ('Truck', 'Truck'),
        ('Coupes', 'Coupes'),
        ('OTHER', 'OTHER'),

    )
    driver = models.OneToOneField(User, on_delete=models.CASCADE)
    vehicleType = models.CharField(max_length=100)
    licensePlate = models.CharField(max_length=100)
    maxPassengers = models.IntegerField()
    def __str__(self):
        return f'{self.driver.userprofile.name} Profile'


