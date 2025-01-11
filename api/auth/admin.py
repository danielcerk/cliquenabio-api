from django.contrib import admin
from .models import UserProfile

@admin.register(UserProfile)
class UserProfileModelAdmin(admin.ModelAdmin):

    list_display= ('name', 'first_name', 
                   'last_name', 'email', 'is_superuser')
    list_filter = ('is_superuser',)
