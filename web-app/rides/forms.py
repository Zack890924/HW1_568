from django import forms
from .models import Ride, RideShare


class RideRequestForm(forms.ModelForm):
    class Meta:
        model = Ride
        fields = ['destination', 'date', 'time', 'owner_passengers',
                  'can_shared', 'special_request', 'vehicle_type_request']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
        }

class RideShareForm(forms.ModelForm):
    class Meta:
        model = RideShare
        fields = ['passenger']
        widgets = {
            'passenger': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
        }



class BaseRideShareForm(forms.Form):
    earliest_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date'}),
        label='Earliest Date'
    )
    latest_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date'}),
        label='Latest Date'
    )

    earliest_time = forms.DateTimeField(
        required=False,
        widget=forms.TimeInput(attrs={'type': 'datetime-local'}),
        label='Earliest Time'
    )
    latest_time = forms.DateTimeField(
        required=False,
        widget=forms.TimeInput(attrs={'type': 'datetime-local'}),
        label='Latest Time'
    )

    def clean(self):
        cleaned_data = super().clean()
        earliest_date = cleaned_data.get('earliest_date')
        latest_date = cleaned_data.get('latest_date')
        earliest_time = cleaned_data.get('earliest_time')
        latest_time = cleaned_data.get('latest_time')

        if earliest_date and latest_date and earliest_date > latest_date:
            raise forms.ValidationError("The earliest date must be before the latest date.")

        if earliest_time and latest_time and earliest_time > latest_time:
            raise forms.ValidationError("The earliest time must be before the latest time.")

        return cleaned_data



class SearchRideShareForm(BaseRideShareForm):
    destination = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Destination'}))

    passengers_size = forms.IntegerField(
        required=False,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
        label = 'Passengers Size'
    )

    def clean_passengers_size(self):
        passengers_size = self.cleaned_data.get('passengers_size')
        if passengers_size is not None and passengers_size < 1:
            raise forms.ValidationError("Passengers size must be at least 1.")
        return passengers_size

class DriverSearchForm(BaseRideShareForm):
    destination = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Destination'}))

    vehicle_type = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Vehicle Type'})
    )



