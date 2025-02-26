from . import views
from django.urls import path
from .views import RideCreateView

app_name = 'rides'

urlpatterns = [
    # path('', views.home, name='rides-home'),
    path('ride-create/', RideCreateView.as_view(), name='ride-create'),
    path('ride-list/', views.OpenRideListView.as_view(), name='ride-list'),
    path('my-ride-list/', views.MyRidesView.as_view(), name='my-ride-list'),
    path('ride-detail/<int:pk>', views.RideDetailView.as_view(), name='ride-detail'),
    path('ride-edit/<int:pk>', views.RideEditView.as_view(), name='ride-edit'),
    path('ride/<int:pk>/cancel/', views.RideCancelView.as_view(), name='ride-cancel'),
    path('ride-join/<int:pk>', views.ride_join, name='ride-join'),
    path('driver-claim/<int:pk>/', views.driver_claim_ride, name='driver_claim_ride'),
    path('driver-complete/<int:pk>/', views.driver_complete_ride, name='driver_complete_ride'),
    path('ride/<int:pk>/quit/', views.RideQuitView.as_view(), name='ride-quit'),


]