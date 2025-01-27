# rides/mixins.py
from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.checks import messages
from django.shortcuts import redirect


class DriverRequiredMixin(UserPassesTestMixin):
    # check if the user is a driver
    def test_func(self):
        return hasattr(self.request.user, 'driverprofile')
    def handle_no_permission(self):
        messages.error(self.request, 'You must be a driver to access this page')
        return redirect('rides:ride-create')


class OwnerRequiredMixin(UserPassesTestMixin):
    # check if the user is the owner
    def test_func(self):
        return self.request.user == self.get_object().owner.user
    def handle_no_permission(self):
        messages.error(self.request, 'You must be the owner to access this page')
        return redirect('rides:ride-list')

class RideStatusOpenMixin(UserPassesTestMixin):
    # check if the ride is open
    def test_func(self):
        return self.get_object().status == 'OPEN'
    def handle_no_permission(self):
        messages.error(self.request, 'The ride is not open')
        return redirect('rides:ride-list')






