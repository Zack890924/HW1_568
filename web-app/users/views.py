from django.contrib.auth.decorators import login_required
from django.contrib.messages.context_processors import messages
from django.shortcuts import render, redirect
from .forms import UserRegisterForm, UserUpdateForm, UserProfileForm, DriverProfileForm
# Create your views here.

def register(request):
    form = UserRegisterForm()
    if request.method == 'POST':
        user_form = UserRegisterForm(request.POST)
        profile_form = UserProfileForm(request.POST)
        driver_form = DriverProfileForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            if profile.is_driver:
                if driver_form.is_valid():
                    driver = driver_form.save(commit=False)
                    driver.driver = user
                    driver.save()
                else :
                    messages.error(request, 'Driver form is not valid')
                    return redirect('/')

            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('/')
    else :
        user_form = UserRegisterForm()
        profile_form = UserProfileForm()
        driver_form = DriverProfileForm()
    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'driver_form': driver_form
    }
    return render(request, 'users/register.html', context)





