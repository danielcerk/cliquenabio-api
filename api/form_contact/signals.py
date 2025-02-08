from django.dispatch import receiver

from django.db.models.signals import post_save

from .models import FormContactEmail

from django.conf import settings

User = settings.AUTH_USER_MODEL

@receiver(post_save, sender=User)
def create_form_contact_layout_user(sender, instance, created, **kwargs):
    
    if created and not FormContactEmail.objects.filter(user=instance).exists():
        
        FormContactEmail.objects.create(user=instance)