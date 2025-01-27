from django.db import models
from datetime import datetime
# Create your models here.


class Ride(models.Model):
    class Status(models.TextChoices):
        PENDING = 'PENDING', 'Pending'
        OPEN = 'OPEN', 'Open'
        ACCEPTED = 'ACCEPTED', 'Accepted'
        CONFIRMED = 'CONFIRMED', 'Confirmed'
        COMPLETED = 'COMPLETED', 'Completed'


    owner = models.ForeignKey('users.UserProfile', on_delete=models.CASCADE, related_name='own_ride')
    driver = models.ForeignKey('users.DriverProfile', on_delete=models.CASCADE, related_name= 'drive_ride', null=True, blank=True)
    # passenger = models.ForeignKey('users.UserProfile', on_delete=models.CASCADE, related_name='passenger_ride', null=True, blank=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.OPEN)
    arrived_time = models.DateTimeField()
    destination = models.CharField(max_length=100)
    date = models.DateField()
    time = models.TimeField()
    owner_passengers = models.PositiveIntegerField(default=1)
    can_shared = models.BooleanField(default=False)
    # optional
    special_request = models.CharField(max_length=100, null=True, blank=True)
    vehicle_type_request = models.CharField(max_length=100, null=True, blank=True)

    def total_amount_people(self):
        return self.owner_passengers + sum(ride_share.passenger for ride_share in self.ride_share.all())

    def scheduled_datetime(self):
        return datetime.combine(self.date, self.time)

    def __str__(self):
        return f"{self.owner.name} => {self.destination} {self.date} {self.time} {self.get_status_display()}"


class RideShare(models.Model):
    ride = models.ForeignKey(Ride, on_delete=models.CASCADE, related_name='ride_share')
    sharer = models.ForeignKey('users.UserProfile', on_delete=models.CASCADE, related_name='user_share')
    passenger = models.PositiveIntegerField(default=1)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['ride', 'sharer'], name='unique_sharer_ride')
        ]

    def __str__(self):
        return f"{self.ride} => {self.sharer.name} => {self.passenger}"


