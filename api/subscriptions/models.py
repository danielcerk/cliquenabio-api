from datetime import timezone
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Plans(models.Model):

    class Plan(models.TextChoices):

        GRATIS = 'GRÁTIS', 'Grátis'
        CONEXAO = 'CONEXÃO', 'Conexão'
        INFLUENCIA = 'INFLUÊNCIA', 'Influência'

    name = models.CharField(

        max_length=50,
        choices=Plan.choices,
        default=Plan.GRATIS,
        verbose_name='Nome'
        
    )

    description = models.TextField(null=True, blank=True, verbose_name='Descrição')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Preço')
    stripe_price_id = models.CharField(
        max_length=255, null=True, blank=True, verbose_name="Stripe Price ID"
    )  # Relaciona com os preços no Stripe
    active = models.BooleanField(default=True, verbose_name='Ativo')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Criado em')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Atualizado em')

    class Meta:

        verbose_name = 'Plano'
        verbose_name_plural = 'Planos'

    def __str__(self):

        return f'Plano {self.name}'


class Subscription(models.Model):

    plan = models.ForeignKey(Plans, on_delete=models.CASCADE,
        null=True, verbose_name='Plano')

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        verbose_name='Usuário',
        related_name='subscription',
    )
    stripe_customer_id = models.CharField(max_length=255, verbose_name="Stripe Customer ID")
    stripe_subscription_id = models.CharField(max_length=255, verbose_name="Stripe Subscription ID")
    stripe_price_id = models.CharField(
        max_length=255, null=True, blank=True, verbose_name="Stripe Price ID"
    )
    current_period_start = models.DateTimeField(
        null=True, blank=True, verbose_name="Início do período atual"
    )
    current_period_end = models.DateTimeField(
        null=True, blank=True, verbose_name="Fim do período atual"
    )
    cancel_at_period_end = models.BooleanField(
        default=False, verbose_name="Cancelar no final do período"
    )
    active = models.BooleanField(default=False, verbose_name='Ativo')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Criado em')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Atualizado em')

    class Meta:

        verbose_name = 'Plano de assinatura'
        verbose_name_plural = 'Planos de assinatura'

    def __str__(self):

        return f"{self.user.name}"

    def save(self, *args, **kwargs):

        if not self.plan:

            self.plan = Plans.objects.filter(id=1).first()

        super().save(*args, **kwargs)


    def is_active(self):

        if not self.active:

            return False
        
        if self.current_period_end and self.current_period_end < timezone.now():

            return False
        
        return True

