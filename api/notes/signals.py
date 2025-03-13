from django.dispatch import receiver
from django.conf import settings
from django.db.models.signals import post_save, pre_delete

from .models import Note, NoteCount

User = settings.AUTH_USER_MODEL

@receiver(post_save, sender=User)
def create_note_count_user(sender, instance, created, **kwargs):
    
    if created and not NoteCount.objects.filter(owner=instance).exists():
        
        NoteCount.objects.create(owner=instance)

@receiver(pre_delete, sender=Note)
def decrement_note_count_user(sender, instance, **kwargs):

    note_count = NoteCount.objects.get(user=instance.user)
    
    note_count.number = max(note_count.number - 1, 0)
    note_count.save()