from django.contrib import admin
from .models import Subscription, Plans

@admin.register(Plans)
class PlanAdmin(admin.ModelAdmin):

    list_display = ('name', 'description',
        'price', 'active', 'created_at')
    
    list_filter = ('name','active')

@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):

    list_display = ('user', 'plan',
        'active', 'created_at', 'updated_at')
    
    list_filter = ('plan','active')