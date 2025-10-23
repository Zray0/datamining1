# inventory/models.py
from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=64, unique=True)
    slug = models.SlugField(max_length=64, unique=True)
    def __str__(self): return self.name

class Product(models.Model):
    sku = models.CharField(max_length=64, unique=True)
    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, null=True, blank=True, related_name="products")
    margin = models.FloatField(default=0.0)
    quantity = models.PositiveIntegerField(default=0)
    def __str__(self): return f"{self.sku} - {self.name}"
