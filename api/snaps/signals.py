from django.dispatch import receiver

from django.db.models.signals import post_save, pre_delete

from .models import SnapCount, Snap

from django.conf import settings

User = settings.AUTH_USER_MODEL

@receiver(post_save, sender=User)
def create_snap_count_user(sender, instance, created, **kwargs):
    
    if created and not SnapCount.objects.filter(owner=instance).exists():
        
        SnapCount.objects.create(owner=instance)

@receiver(pre_delete, sender=Snap)
def decrement_snap_count_user(sender, instance, **kwargs):

    snap_count = SnapCount.objects.get(owner=instance.created_by)
    
    snap_count.number = max(link_count.number - 1, 0)
    snap_count.save()