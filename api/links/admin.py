from django.contrib import admin

from .models import Link, LinkCount

@admin.register(Link)
class LinkAdmin(admin.ModelAdmin):

    list_display = ('created_by__name', 'url', 'social_network', 'username',
        'created_at', 'updated_at')
    
    list_filter = ('created_by__name', 'social_network')

admin.site.register(LinkCount)