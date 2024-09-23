from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from .models import WeatherData
from django.core.exceptions import ValidationError

class WeatherDataModelTest(TestCase):
    def setUp(self):
        self.weather_data = WeatherData.objects.create(
            year=2022,
            month=1,
            dynamic_data={"temperature": 15, "humidity": 30}
        )

    def test_weather_data_creation_with_invalid_year(self):
        weather_data = WeatherData(year=1800, month=1, dynamic_data={"temperature": 15})
        with self.assertRaises(ValidationError):
            weather_data.full_clean()  # Trigger validation

    def test_weather_data_creation_with_invalid_month(self):
        weather_data = WeatherData(year=2022, month=13, dynamic_data={"temperature": 15})
        with self.assertRaises(ValidationError):
            weather_data.full_clean()  # Trigger validation

    def test_weather_data_update_with_invalid_data(self):
        self.weather_data.month = 13
        with self.assertRaises(ValidationError):
            self.weather_data.full_clean()  # Trigger validation

class WeatherDataAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.weather_data = WeatherData.objects.create(
            year=2022,
            month=1,
            dynamic_data={"temperature": 15}
        )
        self.url = f'/api/v1/weather/{self.weather_data.id}/'  # API versioning

    def test_get_weather_data_not_found(self):
        response = self.client.get('/api/v1/weather/9999/')  # Non-existent ID
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_weather_data_invalid(self):
        data = {'year': 2022, 'month': 13, 'dynamic_data': {"temperature": 20}}  # Invalid month
        response = self.client.put(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_weather_data_invalid_year(self):
        data = {'year': 1800, 'month': 2, 'dynamic_data': {"temperature": 25}}  # Invalid year
        response = self.client.post('/api/v1/weather/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_weather_data_invalid_month(self):
        data = {'year': 2023, 'month': 13, 'dynamic_data': {"temperature": 25}}  # Invalid month
        response = self.client.post('/api/v1/weather/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_weather_data_not_found(self):
        response = self.client.delete('/api/v1/weather/9999/')  # Non-existent ID
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_weather_data_no_change(self):
        data = {'year': 2022, 'month': 1, 'dynamic_data': {"temperature": 15}}  # No change
        response = self.client.put(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)  # Should succeed, no error
