from django.contrib import admin

from .models import Feedback

@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):

    list_display = (
        'user', 'rate', 'comment', 'created_at'
    )

    list_filter = (
        'rate',
    )