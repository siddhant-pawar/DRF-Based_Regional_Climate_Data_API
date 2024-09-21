FROM python:3.10-slim

# Environment variables to prevent bytecode generation and ensure unbuffered output
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends build-essential libpq-dev && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python packages
COPY requirements.txt /app/
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Copy application code
COPY . /app/

# Run migrations and makemigrations
RUN python manage.py makemigrations && \
    python manage.py migrate

# Create superuser if necessary
RUN python manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('sidpawar', 'sidpawar11@gmail.com', 'gamebot')"

# Run the fetch_weather_data management command
RUN python manage.py fetch_weather_data

# Expose the application port
EXPOSE 8000

# Start the Django application with Gunicorn
ENTRYPOINT ["gunicorn", "--bind", "0.0.0.0:8000", "jsonapis.wsgi", "--log-file", "-"]

