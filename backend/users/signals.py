from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import CustomerProfile, User


@receiver(post_save, sender=User)
def create_customer_profile(sender, instance, created, **kwargs):
    """Every user always has a profile so the API never returns a partial object."""
    if created:
        CustomerProfile.objects.get_or_create(user=instance)
