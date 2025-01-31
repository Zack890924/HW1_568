from random import choices

from django import forms
from .models import Ride, RideShare





class RideRequestForm(forms.ModelForm):
    VEHICLE_TYPE_CHOICES = [
        ('', '--- Not Specified ---'),
        ('SUV', 'SUV'),
        ('SEDAN', 'SEDAN'),
        ('Hybrid', 'Hybrid'),
        ('VAN', 'VAN'),
        ('Truck', 'Truck'),
        ('Coupes', 'Coupes'),
        ('OTHER', 'Other'),
    ]

    vehicleType = forms.ChoiceField(
        choices=VEHICLE_TYPE_CHOICES,
        required=True,
        widget=forms.Select(attrs={
            'class': 'form-control',
            'id': 'vehicleType',
            'onchange': "toggleOtherVehicle()"
        }),
        label='Vehicle Type',
    )

    other_vehicleType = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Specify Vehicle Type',
            'id': 'otherVehicleType',
            'style': 'display:none'
        }),
        label='Other Vehicle Type'
    )
    class Meta:
        model = Ride
        fields = ['destination', 'scheduled_datetime', 'owner_passengers',
                  'can_shared', 'special_request']
        widgets = {
            'scheduled_datetime': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'destination': forms.TextInput(attrs={'class': 'form-control'}),
            'owner_passengers': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'can_shared': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'special_request': forms.TextInput(attrs={'class': 'form-control'}),
        }
    def clean(self):
        cleaned_data = super().clean()
        vehicle_type = cleaned_data.get('vehicle_type')
        other_vehicle_type = cleaned_data.get('other_vehicleType')
        if vehicle_type == 'OTHER':
            if not other_vehicle_type:
                self.add_error('other_vehicleType', 'Please enter a vehicle type.')
            else:
                cleaned_data['vehicle_type'] = other_vehicle_type

        return cleaned_data








class RideShareForm(forms.ModelForm):
    class Meta:
        model = RideShare
        fields = ['passenger']
        widgets = {
            'passenger': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
        }



class BaseRideShareForm(forms.Form):
    earliest_datetime = forms.DateTimeField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
        label='Earliest Time'
    )
    latest_datetime = forms.DateTimeField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
        label='Latest Time'
    )


    def clean(self):
        cleaned_data = super().clean()
        earliest_datetime = cleaned_data.get('earliest_datetime')
        latest_datetime = cleaned_data.get('latest_datetime')


        if earliest_datetime and latest_datetime and earliest_datetime> latest_datetime:
            raise forms.ValidationError("The earliest time must be before the latest time.")
        return cleaned_data



class SearchRideShareForm(BaseRideShareForm):
    VEHICLE_TYPE_CHOICES = [
        ('SUV', 'SUV'),
        ('SEDAN', 'SEDAN'),
        ('Hybrid', 'Hybrid'),
        ('VAN', 'VAN'),
        ('Truck', 'Truck'),
        ('Coupes', 'Coupes'),
        ('OTHER', 'Other'),
    ]


    destination = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Destination'})
    )

    passengers_size = forms.IntegerField(
        required=False,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
        label = 'Passengers Size'
    )


    vehicle_type = forms.ChoiceField(
        choices = VEHICLE_TYPE_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Vehicle Type'
    )

    other_vehicleType = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Specify Vehicle Type'}),
        label='Other Vehicle Type'
    )



    def clean_passengers_size(self):
        passengers_size = self.cleaned_data.get('passengers_size')
        if passengers_size is not None and passengers_size < 1:
            raise forms.ValidationError("Passengers size must be at least 1.")
        return passengers_size
    def clean (self):
        cleaned_data = super().clean()
        vehicle_type = cleaned_data.get('vehicle_type')
        other_vehicle_type = cleaned_data.get('other_vehicleType')
        if vehicle_type == 'OTHER':
            if not other_vehicle_type:
                self.add_error('other_vehicleType', 'Please enter a vehicle type.')
            else:
                cleaned_data['vehicle_type'] = other_vehicle_type

        return cleaned_data

# TODO vechnicle type
class DriverSearchForm(BaseRideShareForm):
    destination = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Destination'}))

    vehicle_type = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Vehicle Type'})
    )



