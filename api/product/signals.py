from django.dispatch import receiver

from django.db.models.signals import post_save, pre_delete

from .models import ProductCount, Product

from django.conf import settings

User = settings.AUTH_USER_MODEL

@receiver(post_save, sender=User)
def create_product_count_user(sender, instance, created, **kwargs):
    
    if created and not ProductCount.objects.filter(owner=instance).exists():
        
        ProductCount.objects.create(owner=instance)

@receiver(pre_delete, sender=Product)
def decrement_product_count_user(sender, instance, **kwargs):

    product_count = ProductCount.objects.get(owner=instance.created_by)
    
    product_count.number -= 1
    product_count.save()