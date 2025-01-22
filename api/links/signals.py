from django.dispatch import receiver
from django.conf import settings
from django.db.models.signals import post_save, pre_delete

from .models import LinkCount, Link

User = settings.AUTH_USER_MODEL

@receiver(post_save, sender=User)
def create_link_count_user(sender, instance, created, **kwargs):
    
    if created and not LinkCount.objects.filter(owner=instance).exists():
        
        LinkCount.objects.create(owner=instance)

@receiver(pre_delete, sender=Link)
def decrement_link_count_user(sender, instance, **kwargs):

    link_count = LinkCount.objects.get(owner=instance.created_by)
    
    link_count.number -= 1
    link_count.save()