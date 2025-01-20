# Generated by Django 5.1.4 on 2025-01-20 13:04

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('links', '0003_linkcount'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='linkcount',
            options={'ordering': ['-number'], 'verbose_name': 'Contagem de link', 'verbose_name_plural': 'Contagem de links'},
        ),
        migrations.AlterField(
            model_name='link',
            name='created_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Usuário'),
        ),
        migrations.AlterField(
            model_name='link',
            name='username',
            field=models.CharField(blank=True, max_length=255, verbose_name='Nome de usuário:'),
        ),
        migrations.AlterField(
            model_name='linkcount',
            name='number',
            field=models.PositiveBigIntegerField(default=0, verbose_name='Número'),
        ),
        migrations.AlterField(
            model_name='linkcount',
            name='owner',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Usuário'),
        ),
    ]