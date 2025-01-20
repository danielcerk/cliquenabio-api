from django.contrib import admin

from .models import Link, LinkCount

@admin.register(Link)
class LinkAdmin(admin.ModelAdmin):

    list_display = ('created_by', 'url', 'social_network', 'username',
        'created_at', 'updated_at')
    
    list_filter = ('created_by', 'social_network')

@admin.register(LinkCount)
class LinkCountAdmin(admin.ModelAdmin):

    list_display = (
        'owner', 'number'
    )

    list_filter = (
        'owner',
    )