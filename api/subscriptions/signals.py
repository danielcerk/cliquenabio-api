from django.dispatch import receiver
from django.conf import settings
from django.db.models.signals import post_save

from .models import Subscription

User = settings.AUTH_USER_MODEL

@receiver(post_save, sender=User)
def create_subscription_user(sender, instance, created, **kwargs):
    
    if created and not Subscription.objects.filter(user=instance).exists():
        
        Subscription.objects.create(user=instance)