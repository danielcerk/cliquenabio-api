# Generated by Django 5.1.4 on 2025-01-05 12:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profile_user', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='image',
            field=models.URLField(blank=True, null=True, verbose_name='Foto de perfil'),
        ),
    ]