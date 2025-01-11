from django.dispatch import receiver

from django.db.models.signals import post_save

from .models import Profile

from django.conf import settings

User = settings.AUTH_USER_MODEL

@receiver(post_save, sender=User)
def create_profile_user(sender, instance, created, **kwargs):
    
    if created and not Profile.objects.filter(by=instance).exists():
        
        Profile.objects.create(by=instance)