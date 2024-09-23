FROM python:3.10-slim

# Environment variables to prevent bytecode generation and ensure unbuffered output
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set a non-root user for better security
RUN adduser --disabled-password superadmin

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

# Copy application code
COPY . /app/

# Ensure the entrypoint script is copied and executable
COPY entrypoint.sh /app/
RUN chmod +x /app/entrypoint.sh

# Run migrations
RUN python manage.py makemigrations && \
    python manage.py migrate

# Switch to non-root user
USER superadmin

# Health check to ensure the app is running
HEALTHCHECK CMD curl --fail http://localhost:8000/ || exit 1

# Set the entrypoint
ENTRYPOINT ["/app/entrypoint.sh"]

# Expose the application port
EXPOSE 8000
