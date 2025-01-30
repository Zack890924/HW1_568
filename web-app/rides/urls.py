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
    # path('ride-delete/<int:pk>', views.RideDeleteView.as_view(), name='ride-delete'),
    path('ride-join/<int:pk>', views.ride_join, name='ride-join'),

]