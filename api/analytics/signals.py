from django.dispatch import receiver

from django.db.models.signals import post_save

from .models import AnalyticProfileViews

from django.conf import settings

User = settings.AUTH_USER_MODEL

@receiver(post_save, sender=User)
def create_analytic_views_count_user(sender, instance, created, **kwargs):
    
    if created and not AnalyticProfileViews.objects.filter(owner=instance).exists():
        
        AnalyticProfileViews.objects.create(owner=instance)