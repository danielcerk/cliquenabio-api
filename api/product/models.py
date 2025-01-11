from django.db import models

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

User = get_user_model()

class Product(models.Model):

    created_by = models.ForeignKey(User, 
        on_delete=models.CASCADE)

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

        verbose_name = 'Produto'
        verbose_name_plural = 'Produtos'

    def save(self, *args, **kwargs):

        if not self.pk:

            try:

                product_count = ProductCount.objects.get(owner=self.created_by)

            except ProductCount.DoesNotExist:

                raise ValidationError('Perfil associado ao usuário não encontrado.')

            if product_count.number >= 10:

                raise ValidationError('Você não pode adicionar mais de 10 produtos.')

            product_count.number += 1
            product_count.save()

        super().save(*args, **kwargs)


    def delete(self, *args, **kwargs):
        
        try:

            product_count = ProductCount.objects.get(owner=self.created_by)

        except ProductCount.DoesNotExist:
            
            raise ValidationError('Perfil associado ao usuário não encontrado.')

        if product_count.number > 0:

            product_count.number -= 1
            product_count.save()

        super().delete(*args, **kwargs)


    def __str__(self):

        return '%s criado por %s' % (self.name, self.created_by.name)
    
class ProductCount(models.Model):

    owner = models.OneToOneField(User, on_delete=models.CASCADE)
    number = models.PositiveBigIntegerField(default=0)

    def __str__(self):

        return '%s tem %s produto(s)' % (self.owner.name, self.number)