from django.db import models

from django.contrib.auth import get_user_model

User = get_user_model()

class AnalyticProfileViews(models.Model):

    owner = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Usuário')
    number = models.PositiveBigIntegerField(default=0, verbose_name='Número')

    class Meta:

        ordering = ['-number']

    def __str__(self):

        return '%s tem %s views' % (self.owner.name, self.number)

class Analytic(models.Model):
    
    route = models.CharField(max_length=255, unique=False, verbose_name='Rota de perfil')
    month = models.PositiveSmallIntegerField(verbose_name='Mês de criação')
    year = models.PositiveIntegerField(verbose_name='Ano de criação')

    class Meta:

        unique_together = ('route', 'month', 'year')

    def __str__(self):

        return f"{self.route} - {self.month}/{self.year}"