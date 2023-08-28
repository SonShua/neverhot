from django.test import TestCase
from django.urls import reverse
from .models import City, Forecast
from .utils import get_weather_forecast


# Create your tests here.


class CityTestCase(TestCase):
    def setUp(self):
        City.objects.create(city_name="Berlin", lat=52.5170365, lon=13.3888599)

    def test_city_has_values(self):
        berlin = City.objects.get(city_name="Berlin")
        self.assertEqual(berlin.slug, "berlin")


class ForecastTestCase(TestCase):
    def setUp(self):
        # This is the only method used
        berlin = City.objects.create(city_name="Berlin", lat=52.5170365, lon=13.3888599)
        return super().setUp()

    def test_forecast_has_values(self):
        all_forecasts = Forecast.objects.all()
        # Should be 10 elements created and every field should be filled
        for forecast in all_forecasts:
            self.assertEqual(str(forecast.city), "Berlin")
            self.assertGreater(forecast.temp, -20)
            self.assertGreater(forecast.temp_feel, -20)
            self.assertTrue(0 <= forecast.hum <= 100)
            self.assertTrue(forecast.wind_speed)
            self.assertTrue(forecast.icon)

    def test_url_exists_at_correct_location(self):
        berlin = City.objects.get(city_name="Berlin")
        response = self.client.get(reverse("city_detail", kwargs={"slug": berlin.slug}))
        self.assertEqual(response.status_code, 200)
