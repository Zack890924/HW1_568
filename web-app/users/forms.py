#users/forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import UserProfile, DriverProfile

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('This email is already in use.')
        return email





class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['is_driver', 'address', 'phone']


class DriverProfileForm(forms.ModelForm):
    VEHICLE_TYPE_CHOICES = [
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

    # 添加 special_info 属性，用于记录特殊车辆信息
    special_info = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Enter any special vehicle information',
            'rows': 3,
        }),
        label='Special Vehicle Info'
    )

    class Meta:
        model = DriverProfile
        fields = ['vehicleType', 'licensePlate', 'maxPassengers', 'special_info']
        # To do
        # special_info

        widgets = {
            'licensePlate': forms.TextInput(attrs={'class': 'form-control'}),
            'maxPassengers': forms.NumberInput(attrs={'class': 'form-control', 'min' : 1}),

        }
    def clean(self):
        cleaned_data = super().clean()
        vehicle_type = cleaned_data.get('vehicleType')
        other_vehicle_type = cleaned_data.get('other_vehicleType')
        if vehicle_type == 'OTHER':
            if not other_vehicle_type:
                self.add_error('other_vehicleType', 'Please enter a vehicle type.')
            else:
                cleaned_data['vehicleType'] = other_vehicle_type
        return cleaned_data