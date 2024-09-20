from django.db import models
from django.core.exceptions import ValidationError
from datetime import datetime

def validate_month(value):
    if value < 1 or value > 12:
        raise ValidationError(f'Month must be between 1 and 12. Got {value}.')

def validate_year(value):
    current_year = datetime.now().year
    if value < 1850 or value > current_year:
        raise ValidationError(f'Year must be between 1850 and {current_year}. Got {value}.')

class WeatherBase(models.Model):
    year = models.IntegerField(validators=[validate_year], db_index=True, help_text="Year of the weather data.")
    month = models.IntegerField(validators=[validate_month], db_index=True, help_text="Month of the weather data (1-12).")
    value = models.FloatField(null=True, blank=True, help_text="Measured value for the weather metric.")

    class Meta:
        abstract = True
        ordering = ['year', 'month']

    def __str__(self):
        return f"{self.__class__.__name__} - {self.year}-{self.month}: {self.value}"

class Tmax(WeatherBase):
    class Meta:
        unique_together = (('year', 'month'),)
        verbose_name = "Max Temperature"
        verbose_name_plural = "Max Temperatures"

class Tmin(WeatherBase):
    class Meta:
        unique_together = (('year', 'month'),)
        verbose_name = "Min Temperature"
        verbose_name_plural = "Min Temperatures"

class Tmean(WeatherBase):
    class Meta:
        unique_together = (('year', 'month'),)
        verbose_name = "Mean Temperature"
        verbose_name_plural = "Mean Temperatures"

class Rainfall(WeatherBase):
    class Meta:
        unique_together = (('year', 'month'),)
        verbose_name = "Rainfall"
        verbose_name_plural = "Rainfalls"

class Sunshine(WeatherBase):
    class Meta:
        unique_together = (('year', 'month'),)
        verbose_name = "Sunshine"
        verbose_name_plural = "Sunshines"

class Raindays1mm(WeatherBase):
    class Meta:
        unique_together = (('year', 'month'),)
        verbose_name = "Rain Days (1mm)"
        verbose_name_plural = "Rain Days (1mm)"

class AirFrost(WeatherBase):
    class Meta:
        unique_together = (('year', 'month'),)
        verbose_name = "Air Frost"
        verbose_name_plural = "Air Frosts"
