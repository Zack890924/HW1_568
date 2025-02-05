from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from django.shortcuts import render, redirect
from .forms import UserRegisterForm, UserProfileForm, DriverProfileForm
# Create your views here.





def register(request):
    form = UserRegisterForm()
    if request.method == 'POST':
        user_form = UserRegisterForm(request.POST)
        profile_form = UserProfileForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            try:
                with transaction.atomic():
                    user = user_form.save(commit=False)
                    user.email = user_form.cleaned_data.get('email')
                    user.save()

                    profile = profile_form.save(commit=False)
                    profile.user = user
                    profile.name = user.username
                    profile.save()
            except Exception as e:
                messages.error(request, 'encountered error')
                return render(request, 'users/register.html', {'user_form': user_form, 'profile_form': profile_form})


            username = user_form.cleaned_data.get('username')
            password = user_form.cleaned_data.get('password1')
            new_user = authenticate(username=username, password=password)

            if new_user:
                login(request, user)
                if profile.is_driver:
                    return redirect('users:driver_register_step2')
                else:
                    messages.success(request, f'Account created for {username}!')
                    return redirect('home')
            else :
                messages.warning(request, 'account already created')
        else :
            messages.error(request, 'User form is not valid')
    else :
        user_form = UserRegisterForm()
        profile_form = UserProfileForm()
        # driver_form = DriverProfileForm()
    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        # 'driver_form': driver_form
    }
    return render(request, 'users/register.html', context)


@login_required()
def edit_profile(request):
    if request.method == 'POST':
        update_form = UserRegisterForm(request.POST, instance=request.user)
        if update_form.is_valid():
            update_form.save()
            messages.success(request, 'Your profile has been updated')
            return redirect('home')
        else :
            messages.error(request, 'User form is not valid')
    else :
        update_form = UserRegisterForm(instance=request.user)
    return render(request, 'users/edit_profile.html', {'form': update_form})

@login_required()
def become_driver(request):
    if hasattr(request.user, 'driverprofile'):
        messages.info(request, 'You are already a driver')
        return redirect('home')

    if request.method == 'POST':
        driver_form = DriverProfileForm(request.POST)
        if driver_form.is_valid():
            driver = driver_form.save(commit=False)
            driver.driver = request.user
            driver.save()

            user_profile = request.user.userprofile
            user_profile.is_driver = True
            user_profile.save()

            messages.success(request, 'You are now a driver')
            return redirect('home')
        else :
            messages.error(request, 'Driver form is not valid')
    else :
        driver_form = DriverProfileForm()
    return render(request, 'users/become_driver.html', {'form': driver_form})


@login_required()
def update_driver(request):
    try:
        driver = request.user.driverprofile
    except:
        messages.error(request, 'You are not a driver')
        return redirect('home')

    if request.method == 'POST':
        driver_form = DriverProfileForm(request.POST, instance=driver)
        if driver_form.is_valid():
            driver_form.save()
            messages.success(request, 'Your profile has been updated')
            return redirect('home')
        else :
            messages.error(request, 'Driver form is not valid')
    else :
        driver_form = DriverProfileForm(instance=driver)

    return render(request, 'users/update_driver.html', {'form': driver_form})


@login_required()
def driver_register_step2(request):
    if hasattr(request.user, 'driverprofile'):
        messages.info(request, 'You already have a driver profile.')
        return redirect('home')
    if request.method == 'POST':
        driver_form = DriverProfileForm(request.POST)
        if driver_form.is_valid():
            driver = driver_form.save(commit=False)
            driver.driver = request.user
            driver.save()

            request.user.userprofile.is_driver = True
            request.user.userprofile.save()

            messages.success(request, 'You are now a driver')
            return redirect('home')
        else :
            messages.error(request, 'Driver form is not valid')
    else :
        driver_form = DriverProfileForm()
    return render(request, 'users/become_driver_step2.html', {'form': driver_form})


def logout(request):
    if request == 'POST':
        logout(request)
        messages.success(request, 'You have been logged out')
        return render(request, 'users/logout.html')
    else:
        return render(request, 'home')