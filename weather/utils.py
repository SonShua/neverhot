from .models import City, Forecast
import requests
import datetime as dt
import environ
import ratelimit


def get_openweathermap_key():
    env = environ.Env()
    env.read_env()
    api_key = env.str("OPENWEATHERMAP_KEY")
    return api_key


@ratelimit.decorate(key="ip", rate="10/m")
def get_locations(request, location_name):
    """Make API call to openweathermap geocode. Fetch location details (latidude, longitude, country) matching location_name.
    get_or_create object in database-
    Args:
        location_name (str): Location (City,Village,etc.)

    Returns:
        city_created_list: Novel city objects created from API data
        city_get_list: Existing city objects matching API data.
    """
    request_limit = getattr(request.ratelimit, "request_limit")
    search_limit_results = 1
    api_key = get_openweathermap_key()
    url = f"http://api.openweathermap.org/geo/1.0/direct?q={location_name}&limit={search_limit_results}&appid={api_key}"
    city_created_list = []
    city_get_list = []
    nothing_found = False
    limit = True
    if request_limit == 0:
        limit = False
        cities_suggestion = requests.get(url).json()
        nothing_found = True
        if cities_suggestion:
            city_created_list, city_get_list = add_locations_to_db(cities_suggestion)
            nothing_found = False
    return (city_created_list, city_get_list, nothing_found, limit)


def add_locations_to_db(cities_suggestion):
    city_created_list = []
    city_get_list = []
    for city in cities_suggestion:
        city_obj, created = City.objects.get_or_create(
            city_name=city["name"],
            lat=city["lat"],
            lon=city["lon"],
            country=city["country"],
        )
        if created:
            city_created_list.append(city_obj)
        else:
            city_get_list.append(city_obj)
    return (
        city_created_list,
        city_get_list,
    )


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


def get_weather_forecast(slug):
    """API call to openweathermap to get weather forecasts. Create or update (city_pk + datetime) forecasts.

    Args:
        city_pk (int:pk): ID of City object to get forecasts for

    Returns:
        Empty json object when nothing is found.
    """
    api_key = get_openweathermap_key()
    weather_forecast = {}
    try:
        city = City.objects.get(slug=slug)
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
