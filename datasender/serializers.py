from rest_framework import serializers
from .models import WeatherData
from datetime import datetime

class WeatherDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeatherData
        fields = ['id', 'year', 'month', 'dynamic_data']

    def validate_year(self, value):
        """Validate year using the same logic as your model."""
        if not (1836 <= value <= datetime.now().year):
            raise serializers.ValidationError(f'Year must be between 1850 and {datetime.now().year}.')
        return value

    def validate_month(self, value):
        """Validate month using the same logic as your model."""
        if not (1 <= value <= 12):
            raise serializers.ValidationError('Month must be between 1 and 12.')
        return value
