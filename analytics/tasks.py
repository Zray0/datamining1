from celery import shared_task
from django.core.management import call_command

@shared_task
def run_forecast_task(days=30):
    call_command('run_forecast', f'--days={days}')
    return "forecast_done"
