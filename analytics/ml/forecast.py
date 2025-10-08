import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from statsmodels.tsa.holtwinters import ExponentialSmoothing

def simple_moving_average_forecast(sales_df, periods=7, forecast_days=30):
    if sales_df is None or sales_df.empty:
        idx = pd.date_range(start=datetime.today().date(), periods=forecast_days)
        return pd.DataFrame({'forecast_date': idx, 'predicted_demand': [0]*forecast_days})
    sales_df = sales_df.set_index('date').resample('D').sum().fillna(0)
    sales_df['ma'] = sales_df['quantity'].rolling(window=periods, min_periods=1).mean()
    last_ma = sales_df['ma'].iloc[-1]
    forecast_idx = pd.date_range(start=sales_df.index[-1] + pd.Timedelta(days=1), periods=forecast_days)
    predicted = [float(last_ma) for _ in range(forecast_days)]
    return pd.DataFrame({'forecast_date': forecast_idx.date, 'predicted_demand': predicted})

def holt_winters_forecast(sales_df, forecast_days=30):
    if sales_df is None or sales_df.empty:
        return simple_moving_average_forecast(sales_df, forecast_days=forecast_days)
    sales_df = sales_df.set_index('date').resample('D').sum().fillna(0)
    if len(sales_df) < 3:
        return simple_moving_average_forecast(sales_df.reset_index(), forecast_days=forecast_days)
    model = ExponentialSmoothing(sales_df['quantity'], seasonal=None, trend='add', damped_trend=True)
    fit = model.fit(optimized=True)
    pred = fit.forecast(forecast_days)
    idx = pd.date_range(start=sales_df.index[-1] + pd.Timedelta(days=1), periods=forecast_days)
    return pd.DataFrame({'forecast_date': idx.date, 'predicted_demand': pred.values})
