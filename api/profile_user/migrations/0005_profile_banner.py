# Generated by Django 5.1.4 on 2025-03-02 13:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profile_user', '0004_remove_profile_link_count_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='banner',
            field=models.URLField(blank=True, null=True, verbose_name='Foto do banner'),
        ),
    ]
