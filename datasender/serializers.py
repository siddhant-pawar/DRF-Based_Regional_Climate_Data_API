from rest_framework import serializers
from .models import Tmax, Tmin, Tmean, Rainfall, Sunshine, Raindays1mm, AirFrost

class WeatherBaseSerializer(serializers.ModelSerializer):
    class Meta:
        abstract = True
        fields = ['year', 'month', 'value']

class TmaxSerializer(WeatherBaseSerializer):
    class Meta(WeatherBaseSerializer.Meta):
        model = Tmax
        fields = WeatherBaseSerializer.Meta.fields

class TminSerializer(WeatherBaseSerializer):
    class Meta(WeatherBaseSerializer.Meta):
        model = Tmin
        fields = WeatherBaseSerializer.Meta.fields

class TmeanSerializer(WeatherBaseSerializer):
    class Meta(WeatherBaseSerializer.Meta):
        model = Tmean
        fields = WeatherBaseSerializer.Meta.fields

class RainfallSerializer(WeatherBaseSerializer):
    class Meta(WeatherBaseSerializer.Meta):
        model = Rainfall
        fields = WeatherBaseSerializer.Meta.fields

class SunshineSerializer(WeatherBaseSerializer):
    class Meta(WeatherBaseSerializer.Meta):
        model = Sunshine
        fields = WeatherBaseSerializer.Meta.fields

class Raindays1mmSerializer(WeatherBaseSerializer):
    class Meta(WeatherBaseSerializer.Meta):
        model = Raindays1mm
        fields = WeatherBaseSerializer.Meta.fields

class AirFrostSerializer(WeatherBaseSerializer):
    class Meta(WeatherBaseSerializer.Meta):
        model = AirFrost
        fields = WeatherBaseSerializer.Meta.fields
