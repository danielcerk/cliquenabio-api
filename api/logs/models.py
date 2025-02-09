from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class UserLog(models.Model):

    user = models.ForeignKey(User, 
        on_delete=models.CASCADE, verbose_name='Usuário')
    action = models.TextField(verbose_name='Interação')

    timestamp = models.DateTimeField(auto_now_add=True,
        verbose_name='Data/hora')

    class Meta:

        verbose_name = 'Log do usuário'
        verbose_name_plural = 'Logs dos usuários'

    def __str__(self):

        return f'{self.user} - {self.action} ({self.timestamp})'
