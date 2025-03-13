from django.db import models
from django.core.exceptions import ValidationError
from api.subscriptions.models import Subscription
from django.contrib.auth import get_user_model

User = get_user_model()

class NoteCount(models.Model):

    owner = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Usuário')
    number = models.PositiveBigIntegerField(default=0, verbose_name='Número')

    class Meta:

        verbose_name = 'Contagem de nota'
        verbose_name_plural = 'Contagem de Notas'

        ordering = ['-number']

    def __str__(self):

        return '%s tem %s link(s)' % (self.owner.name, self.number)

class Note(models.Model):

    text = models.TextField(
        verbose_name='Texto:'
    )

    user = models.ForeignKey(
        User, on_delete=models.CASCADE,
        verbose_name='Usuário'
    )

    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name='Criado em'
    )
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name='Atualizado em'
    )

    class Meta:

        verbose_name = 'Nota'
        verbose_name_plural = 'Notas'

    def save(self, *args, **kwargs):

        self.text = f'"{self.text}"'

        plan_user = Subscription.objects.get(user=self.user)

        if not self.pk:

            try:

                note_count = NoteCount.objects.get(owner=self.user)

            except NoteCount.DoesNotExist:

                raise ValidationError('Perfil associado ao usuário não encontrado.')
            
            if (plan_user == 1 and plan_user.active) or (plan_user in (2, 3) and not plan_user.active):

                if note_count.number >= 1:

                    raise ValidationError('Você não pode adicionar mais de 1 nota.')
                
            elif plan_user == 2 and plan_user.active:

                if note_count.number >= 6:

                    raise ValidationError('Você não pode adicionar mais de 3 notas.')
                
            elif plan_user == 3 and plan_user.active:

                if note_count.number >= 100:

                    raise ValidationError('Você não pode adicionar mais de 100 notas.')

            note_count.number += 1
            note_count.save()

        super().save(*args, **kwargs)

    def __str__(self):

        return f'{self.text} - {self.user.name}'