from django.db import models
from django.conf import settings
from django.utils import timezone
from inventory.models import Product


class Order(models.Model):
    customer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    created_at = models.DateTimeField(default=timezone.now)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)

    def __str__(self):
        return f"Order {self.pk} - {self.created_at.date()}"

    def calculate_total(self):
        """Recalculate total from related items."""
        total = sum(item.line_total for item in self.items.all())
        self.total_amount = total
        self.save(update_fields=["total_amount"])
        return total


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField()

    def __str__(self):
        return f"{self.product.name} (x{self.quantity})"

    @property
    def line_total(self):
        """Returns total price for this line item."""
        return self.price * self.quantity
