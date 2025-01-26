from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import UserProfile, DriverProfile

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
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