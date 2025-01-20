from django.contrib import admin
from .models import Snap, SnapCount

@admin.register(Snap)
class SnapAdmin(admin.ModelAdmin):

    list_display = ('name', 'small_description', 'created_by',
        'created_at', 'updated_at')
    list_filter = ('name', 'created_by')

@admin.register(SnapCount)
class SnapCountAdmin(admin.ModelAdmin):

    list_display = (
        'owner', 'number'
    )
    list_filter = (
        'owner',
    )