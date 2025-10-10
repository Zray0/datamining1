from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self): return self.name

class Product(models.Model):
    sku = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, related_name='products', on_delete=models.SET_NULL, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock_qty = models.IntegerField(default=0)
    reorder_level = models.IntegerField(default=10)
    expiry_date = models.DateField(null=True, blank=True)
    description = models.TextField(blank=True)
    def __str__(self): return f"{self.name} ({self.sku})"
    @property
    def is_low_stock(self):
        return self.stock_qty <= self.reorder_level



class SupplementData(models.Model):
    id = models.BigAutoField(primary_key=True)
    date = models.DateField()
    product_name = models.CharField(max_length=100)
    category = models.CharField(max_length=50)
    units_sold = models.IntegerField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    revenue = models.DecimalField(max_digits=12, decimal_places=2)
    discount = models.FloatField()
    units_returned = models.IntegerField()
    location = models.CharField(max_length=50)
    platform = models.CharField(max_length=50)
    gender = models.CharField(max_length=20)
    age = models.CharField(max_length=20)
    height_cm = models.CharField(max_length=20)
    weight_kg = models.FloatField()
    body_fat = models.FloatField()
    fitness_level = models.CharField(max_length=50)
    weekly_training = models.CharField(max_length=30)
    training_type = models.CharField(max_length=50)
    supplement = models.CharField(max_length=100)
    supplement_type = models.CharField(max_length=50)
    usage_period_weeks = models.IntegerField()
    usage_frequency_times_week = models.IntegerField()
    diet_type = models.CharField(max_length=50)
    weight_change_kg = models.FloatField()
    body_fat_change = models.FloatField()
    performance_improvement = models.FloatField()
    satisfaction = models.FloatField()

    class Meta:
        db_table = 'inventory_supplementdata'

    def __str__(self):
        return self.product_name
