from tabnanny import verbose
from django.db import models

from django.contrib.auth import get_user_model

User = get_user_model()

class Plan(models.TextChoices):

    GRATIS = 'GRÁTIS', 'Grátis'
    CONEXAO = 'CONEXÃO', 'Conexão'
    INFLUENCIA = 'INFLUÊNCIA', 'Influência'

class PlanBaseModel(models.Model):

    name = models.CharField(max_length=50,
        choices=Plan.choices, default=Plan.GRATIS, verbose_name='Nome')

    class Meta:

        abstract = True

class Plans(PlanBaseModel):

    description = models.TextField(null=True, blank=True, verbose_name='Descrição')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Preço')

    active = models.BooleanField(default=True, verbose_name='Ativo')

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Criado em')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Atualizado em')

    class Meta:

        verbose_name = 'Plano'
        verbose_name_plural = 'Planos'

    def __str__(self):

        return f'Plano {self.name}'


class Subscription(PlanBaseModel):

    user = models.OneToOneField(User,
        on_delete=models.CASCADE, verbose_name='Usuário')
    
    stripe_customer_id = models.CharField(max_length=255)
    stripe_subscription_id = models.CharField(max_length=255)

    active = models.BooleanField(default=True, verbose_name='ativo')

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Criado em')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Atualizado em')

    class Meta:

        verbose_name = 'Plano de assinatura'
        verbose_name_plural = 'Planos de assinatura'

    def __str__(self):

        return f"{self.user.name} - {self.name}"

