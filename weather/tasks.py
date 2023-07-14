from background_task import background
from .models import City
from .utils import get_weather


@background(schedule=60)  # Schedule the task to run every 60 seconds
def schedulded_update_weather():
    print("Tasking")
    for city in City.objects.all():
        print("hello")
        city.temp, city.hum = get_weather(city.lat, city.lon)
        print(city.temp)
        city.save()

    # hardcode the id of berlin and update it, first implementation
