from django.db import models

from django.contrib.auth import get_user_model

User = get_user_model()

# Style types

class ThemeGlobal(models.Model):

    name = models.CharField(max_length=255, verbose_name='Nome')

    background_color = models.CharField(max_length=255, verbose_name='Cor de fundo')
    foreground_color = models.CharField(max_length=255, verbose_name='Cor de fonte')
    font_family = models.CharField(max_length=255, verbose_name='Fonte')

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Criado em')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Atualizado em')

    class Meta:

        verbose_name = 'Tema'
        verbose_name_plural = 'Temas'

    def __str(self):

        return self.name
    
class ThemeUser(models.Model):

    user = models.OneToOneField(User, on_delete=
        models.CASCADE, verbose_name='Usuário')
    
    theme = models.ForeignKey(ThemeGlobal,
        on_delete=models.CASCADE, verbose_name='Tema')
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Criado em')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Atualizado em')

    class Meta:

        verbose_name = 'Tema dos usuários'
        verbose_name_plural = 'Tema do usuário'
    
    def __str__(self):

        return f'{self.user.name} está usando o tema {self.theme.name}'
