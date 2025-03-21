# Generated by Django 5.1.4 on 2025-02-21 01:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('analytics', '0006_alter_analytic_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='analyticprofileviewsperdate',
            name='device_type',
            field=models.CharField(blank=True, max_length=255, verbose_name='Aparelho do usuário:'),
        ),
        migrations.AddField(
            model_name='analyticprofileviewsperdate',
            name='location',
            field=models.CharField(blank=True, max_length=255, verbose_name='Localização:'),
        ),
        migrations.AddField(
            model_name='analyticprofileviewsperdate',
            name='referrer_link',
            field=models.URLField(blank=True, null=True, verbose_name='Origem do trafégo:'),
        ),
    ]
