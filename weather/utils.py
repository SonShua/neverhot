import requests


def get_weather(lat, lon):
    # Put api key to Env IMPORTANT
    api_key = "ab769f949632a08f7f69a9a014a26d97"
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}"
    city_weather = requests.get(url).json()
    temp = kelvin_to_celsius(city_weather["main"]["temp"])
    hum = city_weather["main"]["humidity"]
    return temp, hum


def kelvin_to_celsius(temp):
    return temp - 273.15
