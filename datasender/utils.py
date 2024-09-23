import requests
import os
import logging
import re
from django.conf import settings
from django.db import transaction
from .models import WeatherData

logger = logging.getLogger(__name__)

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
    lines = data.splitlines()
    header_found = False
    records_processed = 0

    for line in lines:
        if not line.strip() or line.startswith('Source:') or line.startswith('Areal values') or 'Last updated' in line:
            continue
        
        if not header_found:
            if line.lower().startswith('year'):
                header_found = True
                continue

        records_processed += process_line(line, dataset)

    logger.info(f"Processed {records_processed} records for dataset: {dataset}")

def process_line(line, dataset):
    """Process a single line of weather data."""
    # Skip lines that don't look like valid data
    if re.match('^\d{4}\s', line) is None:
        logger.warning(f"Skipping irrelevant line: {line}")
        return 0

    parts = line.split()
    
    if len(parts) < 13:
        logger.warning(f"Skipping line due to insufficient parts: {line}")
        return 0

    try:
        year = int(parts[0])
        
        # Store annual value
        annual_value = None if parts[1] == '---' else float(parts[1])
        store_data_in_db(year, 0, {dataset: annual_value})

        # Store monthly values
        for month in range(1, 13):
            month_value = parts[month + 1]  # Offset by 1 due to annual value
            if month_value != '---':
                store_data_in_db(year, month, {dataset: float(month_value)})

        return 1

    except ValueError as e:
        logger.warning(f"Skipping line due to parsing error: {line} | Error: {str(e)}")
        return 0
    except IndexError as e:
        logger.warning(f"Skipping line due to index error: {line} | Error: {str(e)}")
        return 0
    
def store_data_in_db(year, month, weather_data):
    """Store weather data in the database."""
    try:
        logger.info(f"Storing data for year: {year}, month: {month}")
        
        with transaction.atomic():
            weather, created = WeatherData.objects.get_or_create(
                year=year,
                month=month,
                defaults={'dynamic_data': {}}
            )
            
            weather.dynamic_data.update(weather_data)
            weather.save()

            action = "Created" if created else "Updated"
            logger.info(f"{action} data for year: {year}, month: {month}")
    
    except Exception as e:
        logger.error(f"Failed to store data in the database for year: {year}, month: {month} | Error: {e}", exc_info=True)

def process_dataset(dataset):
    """Process a single dataset by fetching, parsing, and storing data."""
    try:
        logger.info(f"Starting to process dataset: {dataset}")

        data = fetch_weather_data(dataset)
        logger.info(f"Fetched {len(data)} bytes of data for {dataset}")

        parse_weather_data(data, dataset)

        check_database_state()

    except Exception as e:
        logger.error(f"Error processing dataset {dataset}: {e}", exc_info=True)

def check_database_state():
    """Check and log the number of records for the weather model in the database."""
    count = WeatherData.objects.count()
    logger.info(f"WeatherData: {count} records")
    return True