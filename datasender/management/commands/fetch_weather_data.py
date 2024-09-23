import os
import logging
from django.core.management.base import BaseCommand
from datasender.utils import process_dataset  # Adjust this import path if necessary

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Fetch weather data and store it in the database'

    def handle(self, *args, **kwargs):
        datasets = [
            'Tmax', 
            'Tmin', 
            'Tmean', 
            'Rainfall', 
            'Sunshine', 
            'Raindays1mm', 
            'AirFrost'
        ]

        for dataset in datasets:
            self.stdout.write(self.style.SUCCESS(f'Processing dataset: {dataset}'))
            try:
                process_dataset(dataset)
                self.stdout.write(self.style.SUCCESS(f'Successfully processed dataset: {dataset}'))
            except Exception as e:
                logger.error(f'Error processing dataset {dataset}: {e}', exc_info=True)
                self.stdout.write(self.style.ERROR(f'Failed to process dataset: {dataset} | Error: {str(e)}'))

        self.stdout.write(self.style.SUCCESS('All datasets processed.'))