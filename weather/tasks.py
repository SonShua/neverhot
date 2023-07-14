from background_task import background
from .models import City
from .utils import get_weather


@background(schedule=60)  # Schedule the task to run every 60 seconds
# Updates all city objects in the database for their temp and hum values with django-background-tasks
def schedulded_update_weather():
    print("Tasking")
    for city in City.objects.all():
        print("hello")
        city.temp, city.hum = get_weather(city.lat, city.lon)
        print(city.temp)
        city.save()
