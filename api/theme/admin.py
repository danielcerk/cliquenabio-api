from django.contrib import admin

from .models import ThemeGlobal, ThemeUser

@admin.register(ThemeGlobal)
class ThemeGlobalAdmin(admin.ModelAdmin):

    list_display = (
        'name', 'background_color',
        'foreground_color', 'font_family',
        'created_at', 'updated_at'
    )

    list_filter = (
        'name', 'font_family', 'created_at'
    )

@admin.register(ThemeUser)
class ThemeUserAdmin(admin.ModelAdmin):

    list_display = (
        'user', 'theme',
        'created_at', 'updated_at'
    )

    list_filter = (
        'user', 'created_at'
    )