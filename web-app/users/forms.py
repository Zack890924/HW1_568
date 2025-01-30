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
    class Meta:
        model = DriverProfile
        fields = ['vehicleType', 'licensePlate', 'maxPassengers']
        # To do
        # special_info

        widgets = {
            'vehicleType': forms.TextInput(attrs={'class': 'form-control'}),
            'licensePlate': forms.TextInput(attrs={'class': 'form-control'}),
            'maxPassengers': forms.NumberInput(attrs={'class': 'form-control', 'min' : 1}),

        }