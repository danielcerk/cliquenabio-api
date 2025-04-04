from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class UserTheme(models.Model):
    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE,
        related_name='theme',
        verbose_name='Usuário'
    )
    
    background_color = models.CharField(
        max_length=255, 
        default='#ffffff',
        verbose_name='Cor de fundo'
    )
    foreground_color = models.CharField(
        max_length=255, 
        default='#000000',
        verbose_name='Cor do texto'
    )
    font_family = models.CharField(
        max_length=255, 
        default='Arial, sans-serif',
        verbose_name='Fonte'
    )
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Criado em')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Atualizado em')

    class Meta:
        verbose_name = 'Tema do usuário'
        verbose_name_plural = 'Temas dos usuários'

    def __str__(self):

        if hasattr(self.user, 'get_username'):
            return f'Tema de {self.user.get_username()}'
        elif hasattr(self.user, 'email'):
            return f'Tema de {self.user.email}'
        elif hasattr(self.user, 'name'):
            return f'Tema de {self.user.name}'
        else:
            return f'Tema de usuário #{self.user_id}'

    def save(self, *args, **kwargs):

        if not self.pk and UserTheme.objects.filter(user=self.user).exists():
            raise ValueError('Este usuário já possui um tema registrado')
        super().save(*args, **kwargs)