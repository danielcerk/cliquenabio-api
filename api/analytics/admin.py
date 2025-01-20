from django.contrib import admin

from .models import Analytic, AnalyticProfileViews

@admin.register(Analytic)
class AnalyticAdmin(admin.ModelAdmin):

    list_display = (
        
        'route', 'month', 'year'

    )

    list_filter = (
        'month', 'year'
    )


@admin.register(AnalyticProfileViews)
class AnalyticProfileViewsAdmin(admin.ModelAdmin):

    list_display = (
        'owner', 'number'
    )

    list_filter = (
        'owner',
    )