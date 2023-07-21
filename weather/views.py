from typing import Any, Dict
from django.db import models
from django.db.models.query import QuerySet
from django.views.generic import ListView, DetailView
from django.http import HttpResponseNotFound
from .models import City, Forecast
from django.shortcuts import render, redirect
from .forms import InputForm
from .utils import get_weather_forecast
from weather.tasks import schedulded_update_weather
import datetime


class CityView(ListView):
    model = City
    template_name = "weather.html"
    schedulded_update_weather()

    def get_queryset(self):
        return self.model.objects.all()


class CityDetailView(ListView):
    """
    Goal: Display a line graph with the forecast data temperatures

    Query all forecast available with active City object (indicated by pk from kwargs)
    Filter it down to only forecasts of the day
    Check if there are enough forecasts for the day, if not get new ones datetime.datetime.date

    Lets say for the beginning i always want to display 10 datapoints (~30 hours into the future)
    So I need the last object from the queryset to have a minimum of 27 hours into the future

    Cases:
    How many objects are needed for the forecast?
        Lets say its 18:00
    """

    model = Forecast
    template_name = "city_detail.html"

    def get_queryset(self):
        """
        Return a queryset which has at least 27 hours of forecast data in the future
        """
        min_future_date_forecast = datetime.datetime.now(
            datetime.timezone.utc
        ) + datetime.timedelta(hours=27)
        queryset = self.model.objects.filter(city__id=self.kwargs["pk"])
        if min_future_date_forecast > getattr(queryset.latest("datetime"), "datetime"):
            get_weather_forecast(str(queryset[0].city))
        return self.model.objects.filter(city__id=self.kwargs["pk"])


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
