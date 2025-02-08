from django.contrib import admin

from .models import Analytic, AnalyticProfileViews, AnalyticProfileViewsPerDate

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

@admin.register(AnalyticProfileViewsPerDate)
class AnalytcProfileViewsPerDateModelAdmin(admin.ModelAdmin):

    list_display = (
        'owner', 'created_at'
    )