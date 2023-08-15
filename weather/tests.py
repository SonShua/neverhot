from django.test import TestCase
from django.urls import reverse
from .models import City, Forecast
from background_task import background
from background_task.tasks import tasks
from .tasks import schedulded_update_weather
from .utils import get_weather_forecast


# Create your tests here.


class CityTestCase(TestCase):
    def setUp(self):
        City.objects.create(city_name="Berlin", lat=52.5170365, lon=13.3888599)

    def test_city_has_values(self):
        berlin = City.objects.get(city_name="Berlin")
        self.assertGreater(berlin.temp, -20)
        self.assertGreater(berlin.hum, 0)
        self.assertIsNotNone(berlin.icon)


class ForecastTestCase(TestCase):
    def setUp(self):
        # This is the only method used
        berlin = City.objects.create(city_name="Berlin", lat=52.5170365, lon=13.3888599)
        get_weather_forecast(berlin.pk)
        # City.objects.create(city_name="Berlin", lat=52.5170365, lon=13.3888599)
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
        response = self.client.get(reverse("city_detail", kwargs={"pk": berlin.pk}))
        self.assertEqual(response.status_code, 200)


# Background db update tasks test


class BackgroundTaskTestCase(TestCase):
    """Checks if background-task schedulded_weather_update is working

    Creates a city, grabs the last_updated (datetime), updates the records,
    grabs last_updated (datetime) again and checks for inequality"""

    def setUp(self):
        City.objects.create(
            city_name="Berlin", lat=52.5170365, lon=13.3888599, temp=20, hum=50
        )

    def test_run_task(self):
        time_creation = City.objects.filter(city_name="Berlin").values("last_updated")[
            0
        ]["last_updated"]
        # Running the task
        schedulded_update_weather.now()
        time_update = City.objects.filter(city_name="Berlin").values("last_updated")[0][
            "last_updated"
        ]
        # After the update the datetime objects should be different
        self.assertNotEqual(time_creation, time_update)
