# inventory/admin.py
from django.contrib import admin
from .models import Product, Category

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name","slug")
    search_fields = ("name","slug")
    prepopulated_fields = {"slug": ("name",)}

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("sku","name","category","margin")  # 'category' is OK; Django resolves FK
    list_filter = ("category",)
    search_fields = ("sku","name")
