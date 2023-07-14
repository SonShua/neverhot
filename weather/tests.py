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
        # Lat, Lon from openweathermap geocode api
        City.objects.create(city_name="Berlin", lat=52.5170365, lon=13.3888599)

    def test_city_has_temp(self):
        berlin = City.objects.get(city_name="Berlin")
        self.assertGreater(berlin.temp, -20)
        self.assertGreater(berlin.hum, 0)


# Background db update tasks test


class BackgroundTaskTestCase(TestCase):
    # Updates the weather and the last_updated in db should also be incremented
    def setUp(self):
        City.objects.create(city_name="Berlin", lat=52.5170365, lon=13.3888599)
        time_now = datetime.datetime.now(datetime.timezone.utc)

    def test_run_task(self):
        # Creates the object and last_updated is filled with datetime now
        # Grabbing the datetime of the object creation
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
