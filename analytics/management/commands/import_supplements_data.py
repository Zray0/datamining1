from django.core.management.base import BaseCommand
import pandas as pd
from inventory.models import SupplementData

class Command(BaseCommand):
    help = 'Import supplements data from Excel'

    def handle(self, *args, **kwargs):
        df = pd.read_excel('C:\\Users\\Cyborg\\Desktop\\datamining\\supplements_project\\supplements_data.xlsx')
        for _, row in df.iterrows():
            SupplementData.objects.create(
                date=row['Date'],
                product_name=row['Product Name'],
                category=row['Category'],
                units_sold=row['Units Sold'],
                price=row['Price'],
                revenue=row['Revenue'],
                discount=row['Discount'],
                units_returned=row['Units Returned'],
                location=row['Location'],
                platform=row['Platform'],
                gender=row['Gender'],
                age=row['Age'],
                height_cm=row['Heightcm'],
                weight_kg=row['Weightkg'],
                body_fat=row['BodyFat'],
                fitness_level=row['FitnessLevel'],
                weekly_training=row['WeeklyTraining'],
                training_type=row['TrainingType'],
                supplement=row['Supplement'],
                supplement_type=row['SupplementType'],
                usage_period_weeks=row['UsagePeriodweeks'],
                usage_frequency_times_week=row['UsageFrequencytimesweek'],
                diet_type=row['DietType'],
                weight_change_kg=row['WeightChangekg'],
                body_fat_change=row['BodyFatChange'],
                performance_improvement=row['PerformanceImprovement'],
                satisfaction=row['Satisfaction1-10']
            )
        self.stdout.write(self.style.SUCCESS('Data imported successfully'))
