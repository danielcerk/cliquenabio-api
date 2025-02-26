from django.shortcuts import get_object_or_404
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.utils.text import slugify
from django.conf import settings

from .models import Profile

User = settings.AUTH_USER_MODEL

@receiver(post_save, sender=User)
def create_profile_user(sender, instance, created, **kwargs):
    
    if created and not Profile.objects.filter(by=instance).exists():
        
        Profile.objects.create(by=instance)

@receiver(post_save, sender=User)
def update_slug(sender, instance, **kwargs):

    profile = get_object_or_404(Profile, by=instance)

    slug_name = slugify(instance.name)

    profile.slug = slug_name

    profile.save()