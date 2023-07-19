from django.db import models
import requests

# Create your models here.


class City(models.Model):
    city_name = models.CharField(max_length=500, null=False, blank=False, unique=True)
    country = models.CharField(max_length=500, null=False, blank=True)
    lat = models.FloatField(null=False, blank=False)
    lon = models.FloatField(null=False, blank=False)
    temp = models.FloatField(null=True, blank=True)
    hum = models.IntegerField(null=True, blank=True)
    # Automatically use datetime from default_timezone when creating/updating
    last_updated = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        """Only ran when object is first created
        Pass a value for temp and hum to avoid api calls for tests"""
        if self.pk is None and self.temp is None and self.hum is None:
            self.get_weather()
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.city_name

    def get_weather(self):
        """
        Sets temperature and humidity of location defined by lat/lon as tuple. Openweathermap api call.
        """
        # SECRETS
        api_key = "ab769f949632a08f7f69a9a014a26d97"
        url = f"https://api.openweathermap.org/data/2.5/weather?lat={self.lat}&lon={self.lon}&appid={api_key}"
        city_weather = requests.get(url).json()
        self.temp = round(city_weather["main"]["temp"] - 273.15, 2)
        self.hum = city_weather["main"]["humidity"]


class Weather(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    temp = models.FloatField(null=True, blank=False)
    temp_feel = models.FloatField(null=True, blank=False)
    hum = models.IntegerField(null=True, blank=False)
    wind_speed = models.FloatField(null=True, blank=False)
    datetime = models.DateTimeField(null=True, blank=False)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.city.city_name
