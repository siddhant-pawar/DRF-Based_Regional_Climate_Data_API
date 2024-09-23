from django.db import models
from django.core.exceptions import ValidationError
from datetime import datetime

def validate_month(value):
    """Ensure the month value is between 1 and 12."""
    if not (1 <= value <= 12):
        raise ValidationError(f'Month must be between 1 and 12. Got {value}.')

def validate_year(value):
    """Ensure the year value is reasonable."""
    current_year = datetime.now().year
    if not (1836 <= value <= current_year):
        raise ValidationError(f'Year must be between 1836 and {current_year}. Got {value}.')

class WeatherData(models.Model):
    year = models.IntegerField(
        validators=[validate_year],
        db_index=True,
        help_text="Year of the weather data."
    )
    month = models.IntegerField(
        validators=[validate_month],
        db_index=True,
        help_text="Month of the weather data (1-12)."
    )
    dynamic_data = models.JSONField( 
        null=True,
        blank=True,
        help_text="Dynamic weather data in key-value pairs."
    )

    class Meta:
        unique_together = (('year', 'month'),)
        ordering = ['year', 'month']
        verbose_name = "Weather Data"
        verbose_name_plural = "Weather Data"

    def __str__(self):
        return f"WeatherData - {self.year}-{self.month}: {self.dynamic_data}"


