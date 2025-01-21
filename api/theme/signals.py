from django.dispatch import receiver

from django.db.models.signals import post_save, pre_delete

from .models import ThemeUser, ThemeGlobal

from django.conf import settings

User = settings.AUTH_USER_MODEL

@receiver(post_save, sender=User)
def create_theme_user(sender, instance, created, **kwargs):
    
    if created and not ThemeUser.objects.filter(user=instance).exists():

        theme_global = ThemeGlobal.objects.get(pk=1)
        
        ThemeUser.objects.create(
            user=instance, theme=theme_global
        )