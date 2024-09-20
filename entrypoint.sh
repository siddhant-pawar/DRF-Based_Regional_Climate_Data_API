#!/bin/bash

# Run the fetch_weather_data management command
python manage.py fetch_weather_data

# Start the Django application with Gunicorn
exec gunicorn --bind 0.0.0.0:8000 jsonapis.wsgi --log-file -
