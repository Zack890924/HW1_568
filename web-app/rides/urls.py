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

]