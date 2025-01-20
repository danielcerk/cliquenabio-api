from django.db import models
from django.core.exceptions import ValidationError
from django.conf import settings

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
    
    url = models.URLField(verbose_name='URL:'
        ,null=False, blank=True)
    social_network = models.CharField(max_length=100,
        verbose_name='Rede social', null=False, blank=True)

    username = models.CharField(max_length=255, 
        null=False, blank=True, verbose_name='Nome de usuário:')

    created_at = models.DateTimeField(auto_now_add=True,
        verbose_name='Criado em')
    updated_at = models.DateTimeField(auto_now=True,
        verbose_name='Atualizado em')
    
    def save(self, *args, **kwargs):

        self.social_network, self.username = extract_username_and_social_network_of_link(self.url)

        if not self.pk:

            try:

                link_count = LinkCount.objects.get(owner=self.created_by)

            except LinkCount.DoesNotExist:

                raise ValidationError('Perfil associado ao usuário não encontrado.')

            if link_count.number >= 2:

                raise ValidationError('Você não pode adicionar mais de 2 links.')

            link_count.number += 1
            link_count.save()

        super().save(*args, **kwargs)

    def __str__(self):

        return '%s (@%s) de %s' % (self.social_network, self.username,
                                   self.created_by.name)