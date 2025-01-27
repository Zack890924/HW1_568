from django.db import models
from django.contrib.auth.models import User
from PIL import Image
# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    is_driver = models.BooleanField(default=False)
    address = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    # image = models.ImageField(default='default.jpg', upload_to='profile_pics',blank=True, null=True)
    def __str__(self):
        return f'{self.user.name} Profile'
    # def save (self, *args, **kwargs):
    #     super().save(*args, **kwargs)
    #     img = Image.open(self.image.path)
    #     if img.height > 300 or img.width > 300:
    #         output_size = (300, 300)
    #         img.thumbnail(output_size)
    #         img.save(self.image.path)
class DriverProfile(models.Model):
    driver = models.OneToOneField(User, on_delete=models.CASCADE)
    vehicleType = models.CharField(max_length=100)
    licensePlate = models.CharField(max_length=100)
    maxPassengers = models.IntegerField()
    def __str__(self):
        return f'{self.driver.name} Profile'


