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


class CityView(ListView):
    model = City
    template_name = "weather.html"
    schedulded_update_weather()

    def get_queryset(self):
        return self.model.objects.all()


class CityDetailView(ListView):
    model = Forecast
    template_name = "city_detail.html"

    def get_object(self):
        # View gets pk from City, is also fk in Forecast
        # Backward search from fk field in Forecast (city)
        return self.model.objects.get(city__id=self.kwargs["pk"])


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
