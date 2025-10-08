from django.db import models
from inventory.models import Product

class ForecastData(models.Model):
    product = models.ForeignKey(Product, related_name='forecasts', on_delete=models.CASCADE)
    forecast_date = models.DateField()
    predicted_demand = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    model_name = models.CharField(max_length=100, default='moving_average')
    accuracy = models.FloatField(null=True, blank=True)
    class Meta:
        unique_together = ('product', 'forecast_date')
    def __str__(self):
        return f"{self.product.name} - {self.forecast_date}: {self.predicted_demand}"
