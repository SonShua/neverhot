from .models import City, Forecast
import requests
import datetime as dt
import environ


def get_openweathermap_key():
    env = environ.Env()
    env.read_env()
    api_key = env.str("OPENWEATHERMAP_KEY")
    return api_key


def get_locations(location_name):
    """Fetch location details (latidude, longitude, country) matching passed location_name
    Args:
        location_name (str): Location (City,Village,etc.)

    Returns:
        city_list: City objects matching given name
    """
    limit_results = 5
    api_key = get_openweathermap_key()
    url = f"http://api.openweathermap.org/geo/1.0/direct?q={location_name}&limit={limit_results}&appid={api_key}"
    cities_suggestion = requests.get(url).json()
    i = 0
    city_list = []
    for i in range(0, (limit_results - 1)):
        obj, created = City.objects.get_or_create(
            city_name=cities_suggestion[i]["name"],
            lat=cities_suggestion[i]["lat"],
            lon=cities_suggestion[i]["lon"],
            country=cities_suggestion[i]["country"],
        )
        city_list.append(obj)
    return city_list


def get_weather(lat, lon):
    """
    Sets temperature and humidity of location defined by lat/lon as tuple. Openweathermap api call.
    """
    # SECRETS
    api_key = get_openweathermap_key()
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}"
    city_weather = requests.get(url).json()
    temp = round(city_weather["main"]["temp"] - 273.15, 2)
    hum = city_weather["main"]["humidity"]
    icon = city_weather["weather"][0]["icon"]
    return temp, hum, icon


def get_weather_forecast(city_pk):
    """API call to openweathermap to get weather forecasts. Create or update (city_pk + datetime).

    Args:
        city_pk (int:pk): ID of City object to get forecasts for

    Returns:
        Empty json object when nothing is found.
    """
    api_key = get_openweathermap_key()
    weather_forecast = {}
    try:
        city = City.objects.get(id=city_pk)
        url = f"http://api.openweathermap.org/data/2.5/forecast?lat={city.lat}&lon={city.lon}&appid={api_key}"
        weather_forecast = requests.get(url).json()
        # range controls how far the forecast reaches, max is 38 (16 day forecast?)
        # forecast is in three hour intervals (0,3,6,9,12,15,etc)
        for x in range(0, 12):
            datetime = dt.datetime.strptime(
                # Datetime is delivered in UTC, creates an aware datetime object
                weather_forecast["list"][x]["dt_txt"] + " +0000",
                # %z is the offset to UTC
                f"%Y-%m-%d %H:%M:%S %z",
            )
            # Checks db a forecast for that city + datetime exists. If yes -> update object. If no -> create object.
            Forecast.objects.update_or_create(
                city=city,
                datetime=datetime,
                dt_naive=is_dt_naive(datetime),
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
                    "dt_naive": is_dt_naive(datetime),
                },
            )
    except City.DoesNotExist:
        return weather_forecast


def is_dt_naive(datetime):
    if datetime.tzinfo == None:
        return True
    else:
        return False
