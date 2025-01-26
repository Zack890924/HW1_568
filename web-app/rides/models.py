from django.db import models

# Create your models here.


class Ride(models.Model):
    RIDE_STATUS = (
        ('Pending', 'Pending'),
        ('OPEN', 'Open'),
        ('Accepted', 'Accepted'),
        ('CONFIRMED', 'Confirmed'),
        ('COMPLETED', 'Completed')
    )
    owner = models.ForeignKey('users.UserProfile', on_delete=models.CASCADE, related_name='own_ride')
    driver = models.ForeignKey('users.DriverProfile', on_delete=models.CASCADE, related_name= 'drive_ride', null=True, blank=True)
    passenger = models.ForeignKey('users.UserProfile', on_delete=models.CASCADE, related_name='passenger_ride', null=True, blank=True)
    status = models.CharField(max_length=20, choices=RIDE_STATUS, default='Open')
    arrived_time = models.DateTimeField()
    destination = models.CharField(max_length=100)
    date = models.DateField()
    time = models.TimeField()
    owner_passengers = models.PositiveIntegerField(default=1)
    can_shared = models.BooleanField(default=False)
    # optional
    special_request = models.CharField(max_length=100, null=True, blank=True)
    vehicle_type_request = models.CharField(max_length=100, null=True, blank=True)

    # def total_passengers(self):
    #

