from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import UserTheme
from django.core.cache import cache

User = get_user_model()

@receiver(post_save, sender=User)
def create_or_update_user_theme(sender, instance, created, **kwargs):
    """
    Signal para criar ou atualizar o tema do usuário automaticamente
    """
    if created:

        UserTheme.objects.create(
            user=instance,
            background_color='#ffffff',
            foreground_color='#000000',
            font_family='Arial, sans-serif'
        )
    else:

        UserTheme.objects.get_or_create(
            user=instance,
            defaults={
                'background_color': '#ffffff',
                'foreground_color': '#000000',
                'font_family': 'Arial, sans-serif'
            }
        )

    cache.delete(f'user_theme_{instance.id}')

@receiver(post_delete, sender=UserTheme)
def clear_theme_cache(sender, instance, **kwargs):
    """
    Limpa o cache quando um tema é deletado
    """
    cache.delete(f'user_theme_{instance.user_id}')

@receiver(post_save, sender=UserTheme)
def update_theme_cache(sender, instance, **kwargs):
    """
    Atualiza o cache quando o tema é modificado
    """
    cache.set(
        f'user_theme_{instance.user_id}',
        {
            'background_color': instance.background_color,
            'foreground_color': instance.foreground_color,
            'font_family': instance.font_family
        },
        timeout=60*60*24  # Cache por 24 horas
    )