#!/bin/bash

# Run the fetch_weather_data management command
python manage.py fetch_weather_data

# Start the Django application
exec python manage.py runserver 0.0.0.0:8000
