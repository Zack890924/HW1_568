from django.db import models
from django.utils import timezone



# Create your models here.


class Ride(models.Model):
    class Status(models.TextChoices):
        # PENDING = 'PENDING', 'Pending'
        OPEN = 'OPEN', 'Open'
        CLOSED = 'CLOSED', 'Closed'
        # ACCEPTED = 'ACCEPTED', 'Accepted'
        CONFIRMED = 'CONFIRMED', 'Confirmed'
        COMPLETED = 'COMPLETED', 'Completed'


    owner = models.ForeignKey('users.UserProfile', on_delete=models.CASCADE, related_name='own_ride')
    driver = models.ForeignKey('users.DriverProfile', on_delete=models.SET_NULL, null=True, related_name= 'drive_ride', blank=True)
    # passenger = models.ForeignKey('users.UserProfile', on_delete=models.CASCADE, related_name='passenger_ride', null=True, blank=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.OPEN)
    # arrived_time = models.DateTimeField()
    destination = models.CharField(max_length=100)
    scheduled_datetime = models.DateTimeField()
    owner_passengers = models.PositiveIntegerField(default=1)
    can_shared = models.BooleanField(default=False)
    # optional
    special_request = models.CharField(max_length=100, null=True, blank=True)
    vehicle_type_request = models.CharField(max_length=100, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    def total_amount_people(self):
        return self.owner_passengers + sum(rs.passenger for rs in self.ride_share.all())

    def __str__(self):
        return f"{self.owner.name} => {self.destination} {self.scheduled_datetime} {self.get_status_display()}"


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


