from django.db import models
from .managers import CityManager
from .utils import get_weather

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
            self.temp, self.hum = get_weather(self.lat, self.lon)
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.city_name
