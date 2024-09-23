#!/bin/sh

# Create superuser if not exists
python manage.py createsuperuser --noinput --username "$SUPERUSER_NAME" --email "$SUPERUSER_EMAIL" || true

# Start the Gunicorn server
exec gunicorn --bind 0.0.0.0:8000 jsonapis.wsgi --log-file - --workers 3 --timeout 120

