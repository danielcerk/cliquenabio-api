from django.db import models

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

from api.subscriptions.models import Subscription

User = get_user_model()

class Snap(models.Model):

    created_by = models.ForeignKey(User, 
        on_delete=models.CASCADE, verbose_name='Usuário')

    name = models.CharField(max_length=55,
        verbose_name='Nome', null=False, blank=False)
    small_description = models.CharField(max_length=255,
        verbose_name='Descrição', null=True, blank=True) # The description is small

    image = models.URLField(verbose_name='URL da imagem:',
        default='https://static.vecteezy.com/system/resources/previews/004/141/669/non_2x/no-photo-or-blank-image-icon-loading-images-or-missing-image-mark-image-not-available-or-image-coming-soon-sign-simple-nature-silhouette-in-frame-isolated-illustration-vector.jpg',
        null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True,
        verbose_name='Criado em')
    updated_at = models.DateTimeField(auto_now=True,
        verbose_name='Atualizado em')
    
    class Meta:

        verbose_name = 'Snap'
        verbose_name_plural = 'Snaps'

    def save(self, *args, **kwargs):

        plan_user = Subscription.objects.get(user=self.created_by)

        if not self.pk:

            try:

                snap_count = SnapCount.objects.get(owner=self.created_by)

            except SnapCount.DoesNotExist:

                raise ValidationError('Perfil associado ao usuário não encontrado.')

            if (plan_user == 1 and plan_user.active) or (plan_user in (2, 3) and not plan_user.active):

                if snap_count.number >= 10:

                    raise ValidationError('Você não pode adicionar mais de 10 snaps.')
                
            elif plan_user == 2 and plan_user.active:

                if snap_count.number >= 50:

                    raise ValidationError('Você não pode adicionar mais de 50 snaps.')
                
            elif plan_user == 3 and plan_user.active:

                if snap_count.number >= 1000:

                    raise ValidationError('Você não pode adicionar mais de 1000 snaps.')

            snap_count.number += 1
            snap_count.save()

        super().save(*args, **kwargs)


    def delete(self, *args, **kwargs):
        
        try:

            snap_count = SnapCount.objects.get(owner=self.created_by)

        except SnapCount.DoesNotExist:
            
            raise ValidationError('Perfil associado ao usuário não encontrado.')

        if snap_count.number > 0:

            snap_count.number -= 1
            snap_count.save()

        super().delete(*args, **kwargs)


    def __str__(self):

        return '%s criado por %s' % (self.name, self.created_by.name)
    
class SnapCount(models.Model):

    owner = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Usuário')
    number = models.PositiveBigIntegerField(default=0, verbose_name='Número')

    class Meta:

        verbose_name = 'Contagem de snap'
        verbose_name_plural = 'Contagem de snaps'
        ordering = ['-number']

    def __str__(self):

        return '%s tem %s snap(s)' % (self.owner.name, self.number)