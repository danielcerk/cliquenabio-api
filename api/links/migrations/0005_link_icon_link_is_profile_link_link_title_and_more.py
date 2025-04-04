# Generated by Django 5.1.4 on 2025-02-19 13:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('links', '0004_alter_linkcount_options_alter_link_created_by_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='link',
            name='icon',
            field=models.URLField(blank=True, null=True, verbose_name='URL do ícone:'),
        ),
        migrations.AddField(
            model_name='link',
            name='is_profile_link',
            field=models.BooleanField(default=False, verbose_name='É um link de perfil'),
        ),
        migrations.AddField(
            model_name='link',
            name='title',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Título do link:'),
        ),
        migrations.AlterField(
            model_name='link',
            name='social_network',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Rede social'),
        ),
        migrations.AlterField(
            model_name='link',
            name='username',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Nome de usuário:'),
        ),
    ]
