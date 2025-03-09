from django.db import models
from django.core.exceptions import ValidationError
from django.conf import settings
from api.subscriptions.models import Subscription

from django.core.validators import URLValidator

from .utils import extract_username_and_social_network_of_link

User = settings.AUTH_USER_MODEL

class LinkCount(models.Model):

    owner = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Usuário')
    number = models.PositiveBigIntegerField(default=0, verbose_name='Número')

    class Meta:

        verbose_name = 'Contagem de link'
        verbose_name_plural = 'Contagem de links'

        ordering = ['-number']

    def __str__(self):

        return '%s tem %s link(s)' % (self.owner.name, self.number)

class Link(models.Model):

    created_by = models.ForeignKey(User, 
        verbose_name='Usuário', on_delete=models.CASCADE)
    
    title = models.CharField(
        verbose_name='Título do link:', null=True,
        blank=True, max_length=255
    )
    
    url = models.TextField(verbose_name='URL:', null=False, 
        blank=True, validators=[URLValidator()])
    social_network = models.TextField(
        verbose_name='Rede social', null=True, blank=True)
    
    icon = models.TextField(
        verbose_name='URL do ícone:', null=False, 
        blank=True, validators=[URLValidator()]
    )

    og_image = models.TextField(
        verbose_name='Imagem da Capa:', null=False, 
        blank=True, validators=[URLValidator()]
    )

    username = models.CharField(max_length=255, 
        null=True, blank=True, verbose_name='Nome de usuário:')
    
    is_profile_link = models.BooleanField(
        default=False, verbose_name='É um link de perfil'
    )

    created_at = models.DateTimeField(auto_now_add=True,
        verbose_name='Criado em')
    updated_at = models.DateTimeField(auto_now=True,
        verbose_name='Atualizado em')
    
    def save(self, *args, **kwargs):

        self.social_network, self.username, self.icon, self.og_image = extract_username_and_social_network_of_link(self.url)

        if self.username != 'Sem usuário':

            self.is_profile_link = True

        else:

            self.is_profile_link = False

        plan_user = Subscription.objects.get(user=self.created_by)

        if not self.pk:

            try:

                link_count = LinkCount.objects.get(owner=self.created_by)

            except LinkCount.DoesNotExist:

                raise ValidationError('Perfil associado ao usuário não encontrado.')
            
            if (plan_user == 1 and plan_user.active) or (plan_user in (2, 3) and not plan_user.active):

                if link_count.number >= 2:

                    raise ValidationError('Você não pode adicionar mais de 2 links.')
                
            elif plan_user == 2 and plan_user.active:

                if link_count.number >= 6:

                    raise ValidationError('Você não pode adicionar mais de 6 links.')
                
            elif plan_user == 3 and plan_user.active:

                if link_count.number >= 100:

                    raise ValidationError('Você não pode adicionar mais de 100 links.')

            link_count.number += 1
            link_count.save()

        super().save(*args, **kwargs)

    def __str__(self):

        return '%s de %s' % (
            self.social_network, 
            self.created_by.name
        )