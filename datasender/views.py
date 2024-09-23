from rest_framework import viewsets
from django.shortcuts import render
from django.views import View
from .models import WeatherData
from .serializers import (WeatherDataSerializer)
import logging
from django.http import JsonResponse
import json
from datetime import datetime
# Configure logging
logger = logging.getLogger(__name__)
class HomeView(View):
    def get(self, request):
        wdataset = WeatherData.objects.all()
        metrics = set()

        for data in wdataset:
            if data.dynamic_data:
                metrics.update(data.dynamic_data.keys())

        context = {
            'years': list(range(1836, datetime.now().year + 1)),
            'metrics': sorted(metrics),
            'selected_year': None,
            'selected_month': None,
            'selected_metric': None,
            'dynamic_data': None,
        }

        return render(request, 'index.html', context)

    def post(self, request):
        action = request.POST.get('action')
        year = int(request.POST.get('year'))
        month = int(request.POST.get('month'))

        # Check if the weather data already exists
        weather_data, created = WeatherData.objects.get_or_create(year=year, month=month)

        if action == 'add':
            new_metric = request.POST.get('new_metric')
            new_value = request.POST.get('new_value')

            dynamic_data = weather_data.dynamic_data or {}
            dynamic_data[new_metric] = new_value

            weather_data.dynamic_data = dynamic_data
            weather_data.save()
            return JsonResponse({'success': True, 'message': 'New data added successfully'})

        elif action == 'update':
            old_metric = request.POST.get('old_metric')
            new_metric = request.POST.get('new_metric')
            updated_value = request.POST.get('updated_value')

            dynamic_data = weather_data.dynamic_data or {}

            # Remove old metric if it exists
            if old_metric in dynamic_data:
                del dynamic_data[old_metric]

            # Update or add the new metric with its value
            dynamic_data[new_metric] = updated_value
            weather_data.dynamic_data = dynamic_data
            weather_data.save()
            return JsonResponse({'success': True, 'message': 'Data updated successfully'})

        elif action == 'delete':
            metric_to_delete = request.POST.get('metric_to_delete')
            dynamic_data = weather_data.dynamic_data or {}

            if metric_to_delete in dynamic_data:
                del dynamic_data[metric_to_delete]  # Remove the metric
                weather_data.dynamic_data = dynamic_data
                weather_data.save()
                return JsonResponse({'success': True, 'message': 'Data deleted successfully'})
            else:
                return JsonResponse({'success': False, 'message': 'Metric not found'})

        # Handle selection requests
        selected_metric = request.POST.get('metric')
        dynamic_data = weather_data.dynamic_data or {}
        metric_value = dynamic_data.get(selected_metric, 'No data available')

        context = {
            'years': list(range(1836, datetime.now().year + 1)),
            'metrics': sorted(set(dynamic_data.keys())),
            'selected_year': year,
            'selected_month': month,
            'selected_metric': selected_metric,
            'metric_value': metric_value,
            'dynamic_data': dynamic_data,
        }

        return render(request, 'index.html', context)



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

class WeatherViewSet(BaseWeatherViewSet):
    serializer_class = WeatherDataSerializer
    queryset = WeatherData.objects.all()
