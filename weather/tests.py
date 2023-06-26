from django.test import TestCase
from .models import City

# Create your tests here.


class CityTestCase(TestCase):
    def setUp(self):
        # Lat, Lon from openweathermap geocode api
        City.objects.create(city_name="Berlin", lat=52.5170365, lon=13.3888599)

    def test_city_has_temp(self):
        berlin = City.objects.get(city_name="Berlin")
        self.assertGreater(berlin.temp, -20)
        self.assertGreater(berlin.hum, 0)
