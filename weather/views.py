from typing import Any, Dict
from django.db import models
from django.db.models.query import QuerySet
from django.views.generic import ListView, DetailView
from django.http import Http404, JsonResponse
from .models import City, Forecast
from django.shortcuts import render, redirect
from .forms import InputForm
from .utils import get_weather_forecast
from weather.tasks import schedulded_update_weather
import datetime, pytz, json


class CityView(ListView):
    model = City
    template_name = "weather.html"
    schedulded_update_weather()

    def get_queryset(self):
        return self.model.objects.all()


def sample_bar_chart(self, request):
    queryset = Forecast.objects.filter(city__city_name="Berlin")
    self.kwargs["pk"]
    # Dataset constructor for line chart
    tz = pytz.timezone("Europe/Berlin")
    data = json.dumps(
        [
            dict(
                # Datetime is stored in UTC, need to adjust for local time
                x=forecast.datetime.astimezone(tz).isoformat(),
                y=forecast.temp,
            )
            for forecast in queryset
        ]
    )

    data = {"line": data}
    return render(request, "chart.html", data)


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
            datetime__gte=datetime.datetime.now()
        )
        icon_now = queryset[0].icon
        temp_now = queryset[0].temp
        city_name = City.objects.get(id=self.kwargs["pk"]).city_name
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
        context = {
            "temp": temp_data,
            "temp_feel": temp_feel_data,
            "city_name": city_name,
            "icon_now": icon_now,
            "temp_now": temp_now,
            "forecast_list": queryset,
        }
        return context

    def get_queryset(self):
        """
        Return a queryset which has at least 27 hours of forecast data in the future
        """
        queryset = self.model.objects.filter(city__id=self.kwargs["pk"])
        city_name = City.objects.get(id=self.kwargs["pk"]).city_name
        if not queryset:
            get_weather_forecast(city_name)
        # If not last forecast available is at least 27 hours in the future
        # Trigger API call to get new forecasts
        # Check: last forecast available is at least 27 hours in the future
        # Fail -> Http404
        min_future_date_forecast = datetime.datetime.now(
            datetime.timezone.utc
        ) + datetime.timedelta(hours=27)
        queryset = self.model.objects.filter(city__id=self.kwargs["pk"])
        if min_future_date_forecast > getattr(queryset.latest("datetime"), "datetime"):
            get_weather_forecast(city_name)
            queryset = self.model.objects.filter(city__id=self.kwargs["pk"])
            if min_future_date_forecast > getattr(
                queryset.latest("datetime"), "datetime"
            ):
                raise Http404("No forecast data found")
        return self.model.objects.filter(city__id=self.kwargs["pk"]).filter(
            datetime__gte=datetime.datetime.now()
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
