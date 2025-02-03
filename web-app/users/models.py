
# users/models.py
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator, RegexValidator

# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, null=False, blank=False)
    # email = models.EmailField(unique=True, null=False, blank=False)
    is_driver = models.BooleanField(default=False)
    address = models.CharField(max_length=100)
    phone = models.CharField(
        max_length=20,
        validators=[
            RegexValidator(
                regex=r'^\+?1?\d{9,15}$',
                message='Phone number must be entered in the correct format: +0123456789.'
            )
        ]
    )

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
    # 添加 special_info 字段，允许为空
    special_info = models.TextField(blank=True, null=True, help_text="Enter any special vehicle information")
    def __str__(self):
        return f'{self.driver.userprofile.name} Profile'


