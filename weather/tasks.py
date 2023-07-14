from background_task import background
from .models import City
from .utils import get_weather


@background(schedule=60)
def schedulded_update_weather():
    """Background task

    Pass int argument to change schedule in seconds

    Iterates through every City object and update temp + hum"""
    for city in City.objects.all():
        city.temp, city.hum = get_weather(city.lat, city.lon)
        city.save()
