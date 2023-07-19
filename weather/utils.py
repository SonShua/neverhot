import requests
from .models import City
from .models import Weather
import datetime


def get_geocode(name):
    # SECRETS
    api_key = "ab769f949632a08f7f69a9a014a26d97"
    url = (
        f"http://api.openweathermap.org/geo/1.0/direct?q={name}&limit=5&appid={api_key}"
    )
    cities_suggestion = requests.get(url).json()
    return cities_suggestion


def get_weather_forecast(city_name):
    """API call to openweathermap to get weather forecast. Creates multiple instances of Weather.

    city_name (str) -> Name of a city exisiting in model City"""
    api_key = "ab769f949632a08f7f69a9a014a26d97"
    weather_forecast = {}
    try:
        city = City.objects.get(city_name=city_name)
        url = f"http://api.openweathermap.org/data/2.5/forecast?lat={city.lat}&lon={city.lon}&appid={api_key}"
        weather_forecast = requests.get(url).json()
        # range controls how far the forecast reaches, max is 38 (16 day forecast?)
        # forecast is in three hour intervals (0,3,6,9,12,15,etc)
        for x in range(0, 1):
            Weather.objects.create(
                city=city,
                temp=weather_forecast["list"][x]["main"]["temp"],
                temp_feel=weather_forecast["list"][x]["main"]["feels_like"],
                hum=weather_forecast["list"][x]["main"]["humidity"],
                wind_speed=weather_forecast["list"][x]["wind"]["speed"],
                datetime=datetime.datetime.strptime(
                    weather_forecast["list"][x]["dt_txt"] + " +0000",
                    f"%Y-%m-%d %H:%M:%S %z",
                ),
            )
        return weather_forecast
    except City.DoesNotExist:
        return weather_forecast
