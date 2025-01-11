from tabnanny import verbose
from django.db import models

from django.contrib.auth import get_user_model

User = get_user_model()

class Subscription(models.Model):

    class Plan(models.TextChoices):

        GRATIS = 'GRÁTIS', 'Grátis'
        CONEXAO = 'CONEXÃO', 'Conexão'
        INFLUENCIA = 'INFLUÊNCIA', 'Influência'
        

    user = models.OneToOneField(User,
        on_delete=models.CASCADE)
    
    stripe_customer_id = models.CharField(max_length=255)
    stripe_subscription_id = models.CharField(max_length=255)

    plan = models.CharField(max_length=50,
        choices=Plan.choices, default=Plan.GRATIS)
    active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:

        verbose_name = 'Plano de assinatura'
        verbose_name_plural = 'Planos de assinatura'

    def __str__(self):

        return f"{self.user.name} - {self.plan}"

