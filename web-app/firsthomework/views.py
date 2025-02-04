# homework1/views.py
from django.shortcuts import render
from users.forms import UserRegisterForm, UserProfileForm
def home(request):
    if not request.user.is_authenticated:
        user_form = UserRegisterForm()
        profile_form = UserProfileForm()
    else:
        user_form = None
        profile_form = None
    return render(request, 'home.html', {'user_form': user_form, 'profile_form': profile_form})

