from django.db import models
from .utils import get_weather


class CityManager(models.Manager):
    def create_city(self, city_name):
        city = self.model(
            city_name="worked",
        )
        city.save(using=self._db)
        return city
