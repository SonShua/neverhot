import requests


def get_weather(lat, lon):
    """
    Returns temperature and humidity of location defined by lat/lon as tuple. Openweathermap api call.

    Parameters:
    lat (float) --> Celestial latitude of location
    lon (float) --> Celestial longitude of location)"""
    # SECRETS
    api_key = "ab769f949632a08f7f69a9a014a26d97"
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}"
    city_weather = requests.get(url).json()
    temp = kelvin_to_celsius(city_weather["main"]["temp"])
    hum = city_weather["main"]["humidity"]
    return temp, hum


def kelvin_to_celsius(temp):
    return round(temp - 273.15, 2)


def get_geocode(name):
    # SECRETS
    api_key = "ab769f949632a08f7f69a9a014a26d97"
    url = (
        f"http://api.openweathermap.org/geo/1.0/direct?q={name}&limit=5&appid={api_key}"
    )
    cities_suggestion = requests.get(url).json()
    return cities_suggestion
