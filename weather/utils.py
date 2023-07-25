from .models import City, Forecast
import requests
import datetime


def get_geocode(name):
    # SECRETS
    api_key = "ab769f949632a08f7f69a9a014a26d97"
    url = (
        f"http://api.openweathermap.org/geo/1.0/direct?q={name}&limit=5&appid={api_key}"
    )
    cities_suggestion = requests.get(url).json()
    return cities_suggestion


def get_weather(lat, lon):
    """
    Sets temperature and humidity of location defined by lat/lon as tuple. Openweathermap api call.
    """
    # SECRETS
    api_key = "ab769f949632a08f7f69a9a014a26d97"
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}"
    city_weather = requests.get(url).json()
    temp = round(city_weather["main"]["temp"] - 273.15, 2)
    hum = city_weather["main"]["humidity"]
    icon = city_weather["weather"][0]["icon"]
    return temp, hum, icon


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
        for x in range(0, 12):
            # Checks db if unique_together city + datetime already exists, if yes we just update, otherwise create
            Forecast.objects.update_or_create(
                city=city,
                datetime=datetime.datetime.strptime(
                    # Datetime is delivered in UTC, creates an aware datetime object
                    weather_forecast["list"][x]["dt_txt"] + " +0000",
                    # %z is the offset to UTC
                    f"%Y-%m-%d %H:%M:%S %z",
                ),
                # Fields to update : updated value
                defaults={
                    "temp": round(
                        weather_forecast["list"][x]["main"]["temp"] - 273.15, 2
                    ),
                    "temp_feel": round(
                        weather_forecast["list"][x]["main"]["feels_like"] - 273.15, 2
                    ),
                    "hum": weather_forecast["list"][x]["main"]["humidity"],
                    "wind_speed": weather_forecast["list"][x]["wind"]["speed"],
                    "icon": weather_forecast["list"][x]["weather"][0]["icon"],
                },
            )
    except City.DoesNotExist:
        return weather_forecast
