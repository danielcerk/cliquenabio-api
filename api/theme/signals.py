from django.shortcuts import get_object_or_404
from django.dispatch import receiver

from django.db.models.signals import post_save, pre_delete

from .models import ThemeUser, ThemeGlobal

from django.conf import settings

User = settings.AUTH_USER_MODEL

@receiver(post_save, sender=User)
def create_theme_user(sender, instance, created, **kwargs):
    if created and not ThemeUser.objects.filter(user=instance).exists():
        
        theme_global, created = ThemeGlobal.objects.get_or_create(
            pk=1,
            defaults={
                "name": "Light",
                "background_color": "#fff",
                "foreground_color": "#000",
                "font_family": "Open Sans",
            }
        )

        ThemeUser.objects.create(user=instance, theme=theme_global)
