from django.dispatch import receiver
from django.db.models.signals import post_save
from django.utils.timezone import now

from api.profile_user.models import Profile
from .models import Analytic, AnalyticProfileViews

@receiver(post_save, sender=Profile)
def create_analytic_route_profile(sender, instance, created, **kwargs):

    if created and not Analytic.objects.filter(route=instance.slug).exists():
        
        today = now()

        Analytic.objects.create(
            route=instance.slug,
            month=today.month,
            year=today.year 
        )


@receiver(post_save, sender=Profile)
def create_analytic_route_profile(sender, instance, created, **kwargs):

    if created and not AnalyticProfileViews.objects.filter(owner=instance.by).exists():

        AnalyticProfileViews.objects.create(
            owner=instance.by,
            number=0
        )
