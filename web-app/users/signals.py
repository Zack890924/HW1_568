from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver

from users.models import UserProfile, DriverProfile

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        UserProfilerofile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    if instance.is_driver:
        DriverProfile.objects.get_or_create(driver=instance.user)
    else:
        DriverProfile.objects.filter(driver=instance.user).delete()