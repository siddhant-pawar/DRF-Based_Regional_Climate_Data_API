import requests
import os
import logging
from django.conf import settings
from django.db import transaction, IntegrityError
from django.core.exceptions import ValidationError
from .models import Tmax, Tmin, Tmean, Rainfall, Sunshine, Raindays1mm, AirFrost

logger = logging.getLogger(__name__)

# Mapping of dataset names to their respective models
MODEL_MAPPING = {
    'Tmax': Tmax,
    'Tmin': Tmin,
    'Tmean': Tmean,
    'Rainfall': Rainfall,
    'Sunshine': Sunshine,
    'Raindays1mm': Raindays1mm,
    'AirFrost': AirFrost,
}

def fetch_weather_data(dataset, temp_dir='temp'):
    """Fetch weather data for a specific dataset from a URL or local file."""
    local_file_path = os.path.join(temp_dir, f'{dataset}.txt')
    os.makedirs(temp_dir, exist_ok=True)

    if os.path.exists(local_file_path):
        logger.info(f"Reading data from local file: {local_file_path}")
        with open(local_file_path, 'r') as file:
            data = file.read()
        logger.info(f"Successfully read {len(data)} bytes from local file")
        return data
    else:
        url = f'https://www.metoffice.gov.uk/pub/data/weather/uk/climate/datasets/{dataset}/date/UK.txt'
        try:
            logger.info(f"Fetching data from URL: {url}")
            response = requests.get(url)
            response.raise_for_status()
            data = response.text
            logger.info(f"Successfully fetched {len(data)} bytes from URL")

            with open(local_file_path, 'w') as file:
                file.write(data)
            logger.info(f"Saved fetched data to local file: {local_file_path}")

            return data
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to fetch data from {url}: {str(e)}", exc_info=True)
            raise

def parse_weather_data(data, dataset):
    """Parse the fetched weather data and store it in the database."""
    lines = data.splitlines()
    header_found = False
    records_processed = 0

    for line in lines:
        if not line.strip() or line.startswith('Source:') or line.startswith('Areal values'):
            continue

        if not header_found:
            if line.startswith('year'):
                header_found = True
            continue

        records_processed += process_line(line, dataset)

    logger.info(f"Processed {records_processed} records for dataset {dataset}")

def process_line(line, dataset):
    """Process a single line of weather data."""
    parts = line.split()

    if len(parts) < 13:
        logger.warning(f"Skipping line due to insufficient parts: {line}")
        return 0

    try:
        year = int(parts[0])
        records = 0

        for month_index in range(1, 13):
            value = parts[month_index]
            value = None if value == '---' else float(value)
            if store_data_in_db(year, month_index, value, dataset):
                records += 1
        return records

    except (ValueError, IndexError) as e:
        logger.warning(f"Skipping line due to parsing error: {line} | Error: {str(e)}")
        return 0


def process_dataset(dataset):
    """Process a single dataset by fetching, parsing, and storing data."""
    try:
        logger.info(f"Starting to process dataset: {dataset}")

        # Fetch data
        data = fetch_weather_data(dataset)
        logger.info(f"Fetched {len(data)} bytes of data for {dataset}")
        
        # Parse and store data
        parse_weather_data(data, dataset)

        # Check database state after processing
        check_database_state()

    except Exception as e:
        logger.error(f"Error processing dataset {dataset}: {e}", exc_info=True)


@transaction.atomic
def store_data_in_db(year, month, value, dataset):
    model_mapping = {
        'Tmax': Tmax,
        'Tmin': Tmin,
        'Tmean': Tmean,
        'Rainfall': Rainfall,
        'Sunshine': Sunshine,
        'Raindays1mm': Raindays1mm,
        'AirFrost': AirFrost,
    }

    try:
        model = model_mapping.get(dataset)
        if model:
            instance, created = model.objects.update_or_create(
                year=year, month=month, 
                defaults={'value': value}
            )
            action = "Created" if created else "Updated"
            logger.debug(f"{action} data for {dataset} - Year: {year}, Month: {month}, Value: {value}")
            return True
        else:
            logger.warning(f"Unknown dataset: {dataset}")
            return False
    except Exception as e:
        logger.error(f"Failed to store data in the database: {str(e)}", exc_info=True)
        return False

def check_database_state():
    """Check and log the number of records for each weather model in the database."""
    for model_name, model in MODEL_MAPPING.items():
        count = model.objects.count()
        logger.info(f"{model_name}: {count} records")
    return True
