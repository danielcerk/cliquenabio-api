from django.contrib import admin

from .models import Note, NoteCount

@admin.register(Note)
class NoteModelAdmin(admin.ModelAdmin):

    list_display = (
        'text', 'user', 'created_at', 'updated_at'
    )

    list_filter = (
        'user', 'created_at'
    )

@admin.register(NoteCount)
class NoteCountAdmin(admin.ModelAdmin):

    list_display = (
        'owner', 'number'
    )

    list_filter = (
        'owner',
    )