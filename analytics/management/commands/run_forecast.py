from django.core.management.base import BaseCommand
from analytics.ml.forecast import simple_moving_average_forecast, holt_winters_forecast
from sales.models import OrderItem
from inventory.models import Product
from analytics.models import ForecastData
import pandas as pd

class Command(BaseCommand):
    help = 'Run demand forecast for all products and save to DB'
    def add_arguments(self, parser):
        parser.add_argument('--days', type=int, default=30, help='Forecast days')
    def handle(self, *args, **options):
        forecast_days = options['days']
        products = Product.objects.all()
        for p in products:
            qset = OrderItem.objects.filter(product=p).values('order__created_at', 'quantity')
            data = []
            for item in qset:
                data.append({'date': item['order__created_at'].date(), 'quantity': item['quantity']})
            df = pd.DataFrame(data)
            if not df.empty:
                df = df.groupby('date').sum().reset_index()
            try:
                forecast_df = holt_winters_forecast(df, forecast_days=forecast_days) if len(df) > 7 else simple_moving_average_forecast(df, periods=7, forecast_days=forecast_days)
            except Exception as e:
                self.stdout.write(self.style.WARNING(f"Error forecasting {p}: {e} - falling back to simple MA"))
                forecast_df = simple_moving_average_forecast(df, periods=7, forecast_days=forecast_days)
            for _, row in forecast_df.iterrows():
                ForecastData.objects.update_or_create(
                    product=p,
                    forecast_date=row['forecast_date'],
                    defaults={'predicted_demand': float(row['predicted_demand']), 'model_name': 'hw' if len(df)>7 else 'ma'}
                )
            self.stdout.write(self.style.SUCCESS(f"Forecasted for {p.name}"))
