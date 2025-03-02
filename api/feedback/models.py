from django.db import models

from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator 

User = get_user_model()

class Feedback(models.Model):

    rate = models.PositiveIntegerField(
        default=0, null=True, blank=True,
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        verbose_name='Nota do App:'
    )

    comment = models.TextField(
        verbose_name='Comentário:'
    )

    user = models.ForeignKey(
        User, on_delete=models.CASCADE,
        verbose_name='Usuário:'
    )

    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name='Criado em:'
    )

    def __str__(self):

        feedback = f'{self.user.name} deu nota {self.rate} para o app'

        return feedback

