from django.db import models

from django.contrib.auth import get_user_model

User = get_user_model()

class AnalyticProfileViews(models.Model):

    owner = models.OneToOneField(User, on_delete=models.CASCADE)
    number = models.PositiveBigIntegerField(default=0)

    class Meta:

        ordering = ['-number']

    def __str__(self):

        return '%s tem %s views' % (self.owner.name, self.number)

class Analytic(models.Model):
    
    route = models.CharField(max_length=255, unique=False)
    month = models.PositiveSmallIntegerField()
    year = models.PositiveIntegerField()

    class Meta:

        unique_together = ('route', 'month', 'year')

    def __str__(self):

        return f"{self.route} - {self.month}/{self.year}"