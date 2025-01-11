from django.db import models

from django.conf import settings
from django.utils.text import slugify

import itertools

User = settings.AUTH_USER_MODEL

class Profile(models.Model):

    by = models.OneToOneField(User, 
        on_delete=models.CASCADE, verbose_name='Usuário')
    
    image = models.URLField(verbose_name='Foto de perfil',
    null=True, blank=True)

    slug = models.SlugField(max_length=100, unique=False,
        verbose_name='Slug', null=True, blank=True)
    
    biografy = models.TextField(null=True, 
        blank=True, verbose_name='Biografia')

    created_at = models.DateTimeField(
        auto_now_add=True, 
        verbose_name='Criado em'
    )
    updated_at = models.DateTimeField(
        auto_now=True, 
        verbose_name='Atualizado em'
    )

    class Meta:

        verbose_name = 'Perfil'
        verbose_name_plural = 'Perfis'

    def save(self, *args, **kwargs):

        if not self.slug or (self.pk and Profile.objects.filter(pk=self.pk).exists() and 
                             Profile.objects.get(pk=self.pk).by.name != self.by.name):
                
            base_slug = slugify(self.by.name)
            
            slug = base_slug
            
            for x in itertools.count(1):
                
                if not Profile.objects.filter(slug=slug).exists():
                    
                    break
                
                slug = f'{base_slug}-{x}'
                
            self.slug = slug

        super().save(*args, **kwargs)

    def __str__(self):
        
        return f'Perfil de {self.by.name} - ( {self.by.full_name} )'

