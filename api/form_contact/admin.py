from django.contrib import admin
from .models import FormContactEmail, ContactEmail

@admin.register(ContactEmail)
class ContactEmailModelAdmin(admin.ModelAdmin):

    list_display = (
        'user', 'sender_email', 'content',
        'created_at', 'updated_at'
    )

    list_filter = (
        'user',
    )

@admin.register(FormContactEmail)
class FormContactEmailModelAdmin(admin.ModelAdmin):

    list_display = (
        'user', 'is_activate', 'created_at', 'updated_at'
    )

    list_filter = (
        'is_activate',
    )