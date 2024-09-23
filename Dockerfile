FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Create a non-root user
RUN adduser --disabled-password superadmin

# Set the working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends build-essential libpq-dev && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python packages
COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy application code
COPY . /app/

# Run migrations
RUN python manage.py makemigrations && \
    python manage.py migrate

# Switch to non-root user
USER superadmin

# Health check to ensure the app is running
HEALTHCHECK CMD curl --fail http://localhost:8000/ || exit 1

# Start the application
CMD sh -c "python manage.py createsuperuser --noinput --username \"$SUPERUSER_NAME\" --email \"$SUPERUSER_EMAIL\" || true && \
            exec gunicorn --bind 0.0.0.0:8000 jsonapis.wsgi --log-file - --workers 3 --timeout 120"

# Expose the application port
EXPOSE 8000

