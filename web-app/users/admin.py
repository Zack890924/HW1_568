from django.contrib import admin

# Register your models here.
from rides.models import Ride, RideShare
@admin.register(Ride)
class RideAdmin(admin.ModelAdmin):
    list_display = ['id', 'owner', 'driver', 'destination', 'status', 'scheduled_datetime']
    search_fields = ['owner__name', 'driver__name', 'destination', 'status']

@admin.register(RideShare)
class RideShareAdmin(admin.ModelAdmin):
    list_display = ['id', 'ride', 'sharer', 'passenger']
    search_fields = ['ride__destination', 'sharer__name']
