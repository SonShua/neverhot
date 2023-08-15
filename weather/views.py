from typing import Any, Dict
from django.db import models
from django.db.models.query import QuerySet
from django.views.generic import ListView, DetailView
from django.http import Http404, JsonResponse
from .models import City, Forecast
from django.shortcuts import render, redirect
from .forms import InputForm
from django.utils.translation import gettext_lazy as _
from .utils import get_weather_forecast
from weather.tasks import schedulded_update_weather
import datetime, pytz, json
import environ
import os


class CityView(ListView):
    model = City
    template_name = "weather.html"
    schedulded_update_weather()

    def get_queryset(self):
        return self.model.objects.all()


def sleep(request):
    if request.htmx:
        import time

        time.sleep(10)


class CityDetailView(ListView):
    """
    Goal: Display a line graph with the forecast data temperatures
    Lets say for the beginning i always want to display 10 datapoints (~30 hours into the future)
    So I need the last object from the queryset to have a minimum of 27 hours into the future

    Cases:
    How many objects are needed for the forecast?
        Lets say its 18:00
    """

    model = Forecast
    template_name = "city_detail.html"

    def get_context_data(self, **kwargs: Any):
        queryset = Forecast.objects.filter(city__id=self.kwargs["pk"]).filter(
            datetime__gte=datetime.datetime.now(datetime.timezone.utc)
        )
        city_name = City.objects.get(id=self.kwargs["pk"]).city_name
        city = City.objects.get(id=self.kwargs["pk"])
        # Dataset constructor for line chart
        tz = pytz.timezone("Europe/Berlin")
        temp_data = json.dumps(
            [
                dict(
                    # Datetime is stored in UTC, return it in isoformat
                    x=forecast.datetime.astimezone(tz).isoformat(),
                    y=forecast.temp,
                )
                for forecast in queryset
            ]
        )
        temp_feel_data = json.dumps(
            [
                dict(
                    # Datetime is stored in UTC, return it in isoformat
                    x=forecast.datetime.astimezone(tz).isoformat(),
                    y=forecast.temp_feel,
                )
                for forecast in queryset
            ]
        )
        temp_trans = _("Temperature [°C]")
        context = {
            "temp": temp_data,
            "temp_feel": temp_feel_data,
            "city": city,
            "city_name": city_name,
            "forecast_list": queryset,
            "temp_trans": temp_trans,
        }
        return context

    def get_queryset(self):
        """
        Return a queryset which has at least 27 hours of forecast data in the future
        """
        queryset = self.model.objects.filter(city__id=self.kwargs["pk"])
        if not queryset:
            get_weather_forecast(self.kwargs["pk"])
        # If not last forecast available is at least 27 hours in the future
        # Trigger API call to get new forecasts
        # Check: last forecast available is at least 27 hours in the future
        # Fail -> Http404
        min_future_date_forecast = datetime.datetime.now(
            datetime.timezone.utc
        ) + datetime.timedelta(hours=27)
        queryset = self.model.objects.filter(city__id=self.kwargs["pk"])
        if min_future_date_forecast > getattr(queryset.latest("datetime"), "datetime"):
            get_weather_forecast(self.kwargs["pk"])
            queryset = self.model.objects.filter(city__id=self.kwargs["pk"])
            if min_future_date_forecast > getattr(
                queryset.latest("datetime"), "datetime"
            ):
                raise Http404("No forecast data found")
        return self.model.objects.filter(city__id=self.kwargs["pk"]).filter(
            datetime__gte=datetime.datetime.now(datetime.timezone.utc)
        )


"""
# Started the features of user search of a city with openweathermap api
# On pause for now, no feature for user to add new city


def CityAddView(request):
    context = {}
    form = InputForm(request.POST or None)
    context["form"] = form
    if request.method == "POST":
        # might need to override the is_valid function to check for alpha chars
        # could implement the cities_suggestion logic into the is_valid method then I wouldn't the extra view
        if form.is_valid():
            cities_suggestions = get_geocode(request.POST["name"])
            if cities_suggestions:
                request.session["cities_suggestions"] = cities_suggestions
                return redirect("city_select")
            else:
                return redirect("no_city_found")
    return render(request, "city_new.html", context)


def CitySelectView(request):
    context = {}
    context["cities_suggestions"] = request.session["cities_suggestions"]
    return render(request, "city_select.html", context)


def NoCityView(request):
    context = {}
    return render(request, "no_city_found.html", context)
 """
