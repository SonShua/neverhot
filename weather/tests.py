from django.test import TestCase
from .models import City
from background_task import background
from background_task.tasks import tasks
from .tasks import schedulded_update_weather
import datetime
import time


# Create your tests here.


class CityTestCase(TestCase):
    def setUp(self):
        City.objects.create(city_name="Berlin", lat=52.5170365, lon=13.3888599)

    def test_city_has_temp(self):
        berlin = City.objects.get(city_name="Berlin")
        self.assertGreater(berlin.temp, -20)
        self.assertGreater(berlin.hum, 0)


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
