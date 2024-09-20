from rest_framework import viewsets
from django.shortcuts import render
from django.views import View
from .models import Tmax, Tmin, Tmean, Rainfall, Sunshine, Raindays1mm, AirFrost
from .serializers import (
    TmaxSerializer, TminSerializer, TmeanSerializer,
    RainfallSerializer, SunshineSerializer,
    Raindays1mmSerializer, AirFrostSerializer
)
import logging

# Configure logging
logger = logging.getLogger(__name__)

class HomeView(View):
    def get(self, request):
        years = list(range(1850, 2101))
        context = {
            'years': years,
            'selected_data': None,
            'selected_metric': None,
        }
        return render(request, 'index.html', context)

    def post(self, request):
        selected_year = request.POST.get('year')
        selected_metric = request.POST.get('metric')

        logger.debug(f"Received Year: {selected_year}, Metric: {selected_metric}")

        if selected_year and selected_metric:
            year = int(selected_year)
            selected_data = None

            model_mapping = {
                'tmax': Tmax,
                'tmin': Tmin,
                'tmean': Tmean,
                'rainfall': Rainfall,
                'sunshine': Sunshine,
                'raindays1mm': Raindays1mm,
                'airfrost': AirFrost,
            }

            selected_data = model_mapping.get(selected_metric).objects.filter(year=year)

            logger.debug(f"Selected Data: {list(selected_data)}")

            context = {
                'years': list(range(1850, 2101)),
                'selected_data': selected_data,
                'selected_metric': selected_metric.capitalize(),
            }

            return render(request, 'index.html', context)

        return self.get(request)

def map_view(request):
    years = list(range(1850, 2101))
    
    context = {
        'years': years,
        'selected_data': None,
        'selected_metric': None,
    }
    
    return render(request, 'map.html', context)


class BaseWeatherViewSet(viewsets.ModelViewSet):
    serializer_class = None
    queryset = None

    def get_queryset(self):
        if self.queryset is None:
            model_class = self.serializer_class.Meta.model
            return model_class.objects.all()
        return self.queryset

    def perform_create(self, serializer):
        try:
            instance = serializer.save()
            logger.info(f"Created {self.serializer_class.Meta.model.__name__} instance: {instance}")
        except Exception as e:
            logger.error(f"Error creating instance: {e}")
            raise

    def perform_update(self, serializer):
        try:
            instance = serializer.save()
            logger.info(f"Updated {self.serializer_class.Meta.model.__name__} instance: {instance}")
        except Exception as e:
            logger.error(f"Error updating instance: {e}")
            raise

    def perform_destroy(self, instance):
        logger.info(f"Deleting {self.serializer_class.Meta.model.__name__} instance: {instance}")
        instance.delete()

class TmaxViewSet(BaseWeatherViewSet):
    serializer_class = TmaxSerializer
    queryset = Tmax.objects.all()

class TminViewSet(BaseWeatherViewSet):
    serializer_class = TminSerializer
    queryset = Tmin.objects.all()

class TmeanViewSet(BaseWeatherViewSet):
    serializer_class = TmeanSerializer
    queryset = Tmean.objects.all()

class RainfallViewSet(BaseWeatherViewSet):
    serializer_class = RainfallSerializer
    queryset = Rainfall.objects.all()

class SunshineViewSet(BaseWeatherViewSet):
    serializer_class = SunshineSerializer
    queryset = Sunshine.objects.all()

class Raindays1mmViewSet(BaseWeatherViewSet):
    serializer_class = Raindays1mmSerializer
    queryset = Raindays1mm.objects.all()

class AirFrostViewSet(BaseWeatherViewSet):
    serializer_class = AirFrostSerializer
    queryset = AirFrost.objects.all()
