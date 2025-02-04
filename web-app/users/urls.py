from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'users'

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('driver/', views.become_driver, name='become_driver'),
    path('update_driver/', views.update_driver, name='update_driver'),
    path('driver_register_step2/', views.driver_register_step2, name='driver_register_step2'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
]