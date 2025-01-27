from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy

from .models import Ride, RideShare
from django.shortcuts import render
from django.views.generic import ListView, CreateView
from .forms import RideRequestForm, DriverSearchForm, SearchRideShareForm, BaseRideShareForm, RideShareForm
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.
class OpenRideListView(ListView):
    model = Ride
    template_name = 'rides/ride_list.html'
    context_object_name = 'rides_list'
    paginate_by = 5
    ordering = ['-scheduled_datetime']

    def get_queryset(self):
        return super().get_queryset().filter(status=Ride.OPEN)
    # TODO destination constraint passenger size... to be added


class MyRideListView(ListView):
    model = Ride
    template_name = 'rides/my_rides_list.html'
    context_object_name = 'rides_list'
    paginate_by = 5
    ordering = ['-scheduled_datetime']

    def get_queryset(self):
        return super().get_queryset().filter(owner=self.request.user)



# owner create ride
class RideCreateView(LoginRequiredMixin, CreateView):
    model = Ride
    form_class = RideRequestForm
    template_name = 'rides/ride_create.html'
    success_url = reverse_lazy('rides: my_ride_list')

    # logic for form created successfully
    def form_valid(self, form):
        form.instance.owner = self.request.user
        form.instance.status = Ride.OPEN
        return super().form_valid(form)


@login_required()
def edit_ride(request, ride_id):
    ride = Ride.get_object_or_404(Ride, id = ride_id, owner = request.user)
    if ride.status != Ride.OPEN:
        messages.error(request, 'Cannot edit the ride')
        return redirect('rides:ride-list')

    if request.method == 'POST':
        form = RideRequestForm(request.POST, instance=ride)
        if form.is_valid():
            form.save()
            messages.success(request, 'Ride updated successfully')
            return redirect('rides:ride-list')
        else :
            messages.error(request, 'Ride form is not valid')
    else :
        form = RideRequestForm(instance=ride)

    return render(request, 'rides/ride_edit.html', {'form': form})


@login_required()
def my_rides(request):
    user = request.user

    owned = Ride.objects.filter(owner=user).exclude(status=Ride.COMPLETED)
    shared = RideShare.objects.filter(user=user).exclude(ride__status=Ride.COMPLETED)
    driver = Ride.objects.filter(driver=user).exclude(status=Ride.COMPLETED)

    return render(request, 'rides/my_rides_list.html', {'owned': owned, 'shared': shared, 'driver': driver})


