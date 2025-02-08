from django.contrib import admin
from .models import UserLog

@admin.register(UserLog)
class UserLogModelAdmin(admin.ModelAdmin):

    list_display = (
        'user', 'action', 'timestamp'
    )