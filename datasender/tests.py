from django.test import TestCase
from .models import Tmax, Tmin, Tmean, Rainfall, Sunshine, Raindays1mm, AirFrost
from django.core.exceptions import ValidationError

class WeatherModelTests(TestCase):

    def setUp(self):
        self.valid_data = {
            'year': 2023,
            'month': 8,
            'value': 30.5
        }

    def test_valid_model_creation(self):
        tmax = Tmax(**self.valid_data)
        tmax.full_clean()  # Ensure validation passes before saving
        tmax.save()
        self.assertEqual(Tmax.objects.count(), 1)

    def test_invalid_month_creation(self):
        for model in [Tmax, Tmin, Rainfall, Sunshine, Raindays1mm, AirFrost]:
            with self.assertRaises(ValidationError):
                model(year=2023, month=13, value=30.5).full_clean()  # Invalid month
            with self.assertRaises(ValidationError):
                model(year=2023, month=0, value=30.5).full_clean()  # Invalid month

    def test_invalid_year_creation(self):
        for model in [Tmax, Tmin, Rainfall, Sunshine, Raindays1mm, AirFrost]:
            with self.assertRaises(ValidationError):
                model(year=1849, month=8, value=30.5).full_clean()  # Invalid year

    def test_unique_year_month(self):
        tmax = Tmax(**self.valid_data)
        tmax.full_clean()
        tmax.save()

        # Attempt to create a duplicate entry
        with self.assertRaises(ValidationError):
            duplicate_tmax = Tmax(year=2023, month=8, value=31.0)
            duplicate_tmax.full_clean()  # This should raise ValidationError

    def test_str_method(self):
        for model in [Tmax, Tmin, Rainfall]:
            instance = model(**self.valid_data)
            instance.full_clean()  # Ensure it passes validation
            instance.save()
            self.assertEqual(str(instance), f"{model.__name__} - {self.valid_data['year']}-{self.valid_data['month']}: {self.valid_data['value']}")

    def test_valid_tmean_creation(self):
        tmean = Tmean(year=2023, month=8, value=20.0)
        tmean.full_clean()  # Ensure validation passes
        tmean.save()
        self.assertEqual(Tmean.objects.count(), 1)

    def test_valid_sunshine_creation(self):
        sunshine = Sunshine(year=2023, month=8, value=150.0)
        sunshine.full_clean()  # Ensure validation passes
        sunshine.save()
        self.assertEqual(Sunshine.objects.count(), 1)

    def test_valid_raindays_creation(self):
        raindays = Raindays1mm(year=2023, month=8, value=5.0)
        raindays.full_clean()  # Ensure validation passes
        raindays.save()
        self.assertEqual(Raindays1mm.objects.count(), 1)

    def test_valid_airfrost_creation(self):
        airfrost = AirFrost(year=2023, month=8, value=2.0)
        airfrost.full_clean()  # Ensure validation passes
        airfrost.save()
        self.assertEqual(AirFrost.objects.count(), 1)
