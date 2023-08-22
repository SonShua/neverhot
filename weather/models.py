from django.db import models
from django.urls import reverse
import requests
from autoslug import AutoSlugField
from django.utils.translation import gettext_lazy as _

# Create your models here.


class City(models.Model):
    city_name = models.CharField(
        verbose_name=_("city_name"), max_length=500, null=False, blank=False
    )
    country = models.CharField(max_length=500, null=False, blank=True)
    lat = models.FloatField(null=False, blank=False)
    lon = models.FloatField(null=False, blank=False)
    icon = models.CharField(null=False, blank=True, max_length=500)
    img_path = models.CharField(max_length=200, default="default.jpg")
    last_updated = models.DateTimeField(auto_now=True)
    added = models.DateTimeField(auto_now_add=True)
    slug = AutoSlugField(populate_from="city_name", unique=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["city_name", "lat", "lon"], name="unique location"
            )
        ]

    def __str__(self):
        return self.city_name

    def get_absolute_url(self):
        return reverse("city_detail", kwargs={"slug": self.slug})


class Forecast(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    temp = models.FloatField(null=False, blank=True)
    temp_feel = models.FloatField(null=False, blank=True)
    hum = models.IntegerField(null=False, blank=True)
    wind_speed = models.FloatField(null=False, blank=True)
    datetime = models.DateTimeField(null=False, blank=True)
    icon = models.CharField(null=False, blank=True, max_length=500)
    last_updated = models.DateTimeField(auto_now=True)
    dt_naive = models.BooleanField()

    class Meta:
        # Don't want double entries
        unique_together = ["city", "datetime"]

    def __str__(self):
        return f"{self.city.city_name} + {self.datetime} + {self.last_updated}"
