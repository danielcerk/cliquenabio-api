from django.dispatch import receiver
from django.conf import settings
from django.db.models.signals import post_save

from .models import Subscription

import stripe

User = settings.AUTH_USER_MODEL
stripe.api_key = settings.STRIPE_SECRET_KEY

@receiver(post_save, sender=User)
def create_subscription_user(sender, instance, created, **kwargs):
    
    if created and not Subscription.objects.filter(user=instance).exists():

        customer = stripe.Customer.create(
            email=instance.email,
            name=instance.name
        )
        
        Subscription.objects.create(user=instance,
            stripe_customer_id=customer['id'])