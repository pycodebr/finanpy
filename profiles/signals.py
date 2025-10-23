"""
Signals for the profiles app.

This module contains signal handlers that automatically create and manage
user profiles when User objects are created or modified.
"""

from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Profile

User = get_user_model()


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    """
    Signal handler that automatically creates a Profile when a User is created.

    This ensures every User has an associated Profile without requiring
    explicit creation in views or forms.

    Args:
        sender: The model class (User) that sent the signal
        instance: The actual User instance being saved
        created: Boolean indicating if this is a new User (True) or update (False)
        **kwargs: Additional keyword arguments from the signal
    """
    if created:
        Profile.objects.create(user=instance)
