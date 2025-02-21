from django.db import models

from django.contrib.auth import get_user_model

User = get_user_model()

# Aqui serve para filtramos valores de forma mais rápido
class AnalyticProfileViews(models.Model):

    owner = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Usuário')
    number = models.PositiveBigIntegerField(default=0, verbose_name='Número')

    def save(self, *args, **kwargs):

        referrer_link = kwargs.pop("referrer_link", "")
        location = kwargs.pop("location", "")
        device_type = kwargs.pop("device_type", "")

        create_view_per_date = AnalyticProfileViewsPerDate.objects.create(
            owner=self.owner,
            number=1,
            referrer_link=referrer_link,
            location=location,
            device_type=device_type
        )


        create_view_per_date.save()

        super().save(*args, **kwargs)

    class Meta:

        ordering = ['-number']
        verbose_name = 'Análise de visualização do perfil'
        verbose_name_plural = 'Análises de visualizações de perfis'

    def __str__(self):

        return '%s tem %s views' % (self.owner.name, self.number)

# Informações de cada view
class AnalyticProfileViewsPerDate(models.Model):

    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Usuário')
    number = models.PositiveBigIntegerField(default=0, verbose_name='Número')
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name='Criado em'
    )

    referrer_link = models.URLField(
        verbose_name='Origem do trafégo:', blank=True,
        null=True
    )
    location = models.CharField(
        verbose_name='Localização:', blank=True,
        null=False, max_length=255
    )
    device_type = models.CharField(
        verbose_name='Aparelho do usuário:', blank=True,
        null=False, max_length=255
    )

    class Meta:

        verbose_name = 'Análise de visualização do perfil por data'
        verbose_name_plural = 'Análises de visualizações de perfis por data'

# Aqui, para criarmos uma rota para o usuário e poder contabilizar as views
class Analytic(models.Model):
    
    route = models.CharField(max_length=255, unique=False, verbose_name='Rota de perfil')
    month = models.PositiveSmallIntegerField(verbose_name='Mês de criação')
    year = models.PositiveIntegerField(verbose_name='Ano de criação')

    class Meta:

        unique_together = ('route', 'month', 'year')
        verbose_name = 'Análise'
        verbose_name_plural = 'Análises'

    def __str__(self):

        return f"{self.route} - {self.month}/{self.year}"