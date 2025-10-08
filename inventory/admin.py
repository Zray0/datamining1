from django.contrib import admin
from .models import Product, Category

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('sku','name','category','price','stock_qty','reorder_level')
    search_fields = ('name','sku')

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass
