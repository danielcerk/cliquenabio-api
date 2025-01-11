from django.contrib import admin
from .models import Product, ProductCount

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):

    list_display = ('name', 'small_description', 'created_by',
        'created_at', 'updated_at')
    list_filter = ('name', 'created_by')

admin.site.register(ProductCount)