from typing import Any, Dict
from django.db.models.query import QuerySet
from django.views.generic import TemplateView, CreateView, ListView
from .models import City
from django.shortcuts import render, redirect
from .forms import InputForm
from .utils import get_geocode
from weather.tasks import schedulded_update_weather


class CityView(ListView):
    model = City
    template_name = "weather.html"
    schedulded_update_weather()

    def get_queryset(self):
        return self.model.objects.all()


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
            cities_suggestions = get_geocode(request.POST["city_name"])
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
