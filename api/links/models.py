from django.db import models
from django.core.exceptions import ValidationError
from django.conf import settings

import re

User = settings.AUTH_USER_MODEL

class LinkCount(models.Model):

    owner = models.OneToOneField(User, on_delete=models.CASCADE)
    number = models.PositiveBigIntegerField(default=0)

    def __str__(self):

        return '%s tem %s link(s)' % (self.owner.name, self.number)

class Link(models.Model):

    created_by = models.ForeignKey(User, 
        verbose_name='Criado por', on_delete=models.CASCADE)
    
    url = models.URLField(verbose_name='URL:'
        ,null=False, blank=True)
    social_network = models.CharField(max_length=100,
        verbose_name='Rede social', null=False, blank=True)

    username = models.CharField(max_length=255, 
        null=False, blank=True, verbose_name='Usuário:')

    created_at = models.DateTimeField(auto_now_add=True,
        verbose_name='Criado em')
    updated_at = models.DateTimeField(auto_now=True,
        verbose_name='Atualizado em')
    
    def save(self, *args, **kwargs):

        self.social_network, self.username = self.extract_social_network_and_username()

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

    '''def delete(self, *args, **kwargs):

        link_count = LinkCount.objects.get(owner=self.created_by)

        link_count.number -= 1      
        link_count.save()

        super().delete(*args, **kwargs)'''

    def extract_social_network_and_username(self):

        patterns = {
            'Facebook': r'facebook\.com\/(?:profile\.php\?id=)?([^\/?&]+)',
            'Instagram': r'instagram\.com\/([^\/?&]+)',
            'Twitter': r'twitter\.com\/([^\/?&]+)',
            'LinkedIn': r'linkedin\.com\/in\/([^\/?&]+)',
            'TikTok': r'tiktok\.com\/@([^\/?&]+)',
            'YouTube': r'youtube\.com\/(?:user|channel)\/([^\/?&]+)',
        }

        for social_network, pattern in patterns.items():

            match = re.search(pattern, self.url)

            if match:

                username = match.group(1)
                
                return social_network, username
            
        return 'Desconhecida', 'Não identificado'

    def __str__(self):

        return '%s (@%s) de %s' % (self.social_network, self.username,
                                   self.created_by.name)