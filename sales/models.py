from django.db import models
from django.conf import settings
from inventory.models import Product


class Order(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        null=True, blank=True, related_name="orders"
    )
    platform = models.CharField(max_length=50, blank=True)
    location = models.CharField(max_length=50, blank=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # change here

    def __str__(self):
        return f"Order {self.pk}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name="order_items")
    quantity = models.PositiveIntegerField(default=1)
    price = models.FloatField(default=0.0)

    def line_total(self):
        return self.quantity * self.price
    
class DashboardStats:
    class Meta:
        verbose_name = "Statistics"
        verbose_name_plural = "Statistics"
        app_label = "sales"  # Grouped under "SALES" in admin
    pass

class DashboardStats(Order):
    class Meta:
        proxy = True
        verbose_name = "Statistics"
        verbose_name_plural = "Statistics"