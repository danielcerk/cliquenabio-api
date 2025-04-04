from django.contrib import admin
from .models import UserTheme  # Importamos apenas o novo modelo

@admin.register(UserTheme)
class UserThemeAdmin(admin.ModelAdmin):
    list_display = (
        'user', 
        'background_color',
        'foreground_color', 
        'font_family',
        'created_at', 
        'updated_at'
    )
    
    list_filter = (
        'font_family',
        'created_at',
        'updated_at'
    )
    
    search_fields = (
        'user__username',
        'user__email',
        'background_color',
        'foreground_color'
    )
    
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Relacionamento', {
            'fields': ('user',)
        }),
        ('Configurações de Tema', {
            'fields': (
                'background_color',
                'foreground_color',
                'font_family'
            )
        }),
        ('Datas', {
            'fields': (
                'created_at',
                'updated_at'
            ),
            'classes': ('collapse',)
        })
    )
