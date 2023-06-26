from typing import Any, Dict
from django.views.generic import TemplateView
from .models import City
import requests


class CityView(TemplateView):
    template_name = "city_index.html"

    def get_context_data(self, *args, **kwargs):
        context = super(CityView, self).get_context_data(*args, **kwargs)
        context["city"] = City.objects.get(city_name="Berlin")
        return context

    # def get_weather(lat,lon):
    # Put api key to Env IMPORTANT
    # api_key = "ab769f949632a08f7f69a9a014a26d97"
    # url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}"
    # city_weather = requests.get(url.json())
