from typing import Any
from django.views.generic import ListView, FormView
from django.http import Http404, HttpRequest, HttpResponse
from .models import City, Forecast
from .forms import CityForm
from .utils import get_locations
from django.shortcuts import render
from django.utils.translation import gettext_lazy as _
from .utils import get_weather_forecast
from timezonefinder import TimezoneFinder
from django_tables2 import SingleTableMixin
from django_filters.views import FilterView
from .tables import CityHTMxTable
from .filters import CityFilter
import datetime
import pytz
import json
from crispy_forms.templatetags.crispy_forms_filters import as_crispy_field
from django.template.context_processors import csrf
from crispy_forms.utils import render_crispy_form


class CityHTMxTableView(SingleTableMixin, FilterView):
    table_class = CityHTMxTable
    queryset = City.objects.all()
    filterset_class = CityFilter
    paginate_by = 15

    def get_template_names(self):
        if self.request.htmx:
            template_name = "partials/city_table_partial.html"
        else:
            template_name = "tables/city_table_htmx.html"

        return template_name


class AddCityView(FormView):
    form_class = CityForm
    template_name = "add_city.html"
    # success_url = reverse_lazy("search")

    def form_valid(self, form: Any):
        if self.request.htmx:
            city_lists = get_locations(self.request, form.cleaned_data["city_name"])
            return render(
                self.request,
                "partials/partial_location_results.html",
                {
                    "city_created_list": city_lists[0],
                    "city_get_list": city_lists[1],
                    "nothing_found": city_lists[2],
                    "limit": city_lists[3],
                },
            )
        return super().form_valid(form)

    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            ctx = {}
            ctx.update(csrf(self.request))
            form_html = render_crispy_form(form, context=ctx)
            return self.form_invalid(form_html)


def check_locationname(request):
    """View function for dynamically validation checking of location name input.
    Could be integrated into SearchView (get method?)"""
    form = CityForm(request.GET)
    context = {
        "field": as_crispy_field(form["city_name"]),
        "valid": not form["city_name"].errors,  # If no errors, valid is set to True
    }
    return render(request, "partials/field.html", context)


class CityView(ListView):
    model = City
    template_name = "weather.html"

    def get_queryset(self):
        return self.model.objects.all()


class CityDetailView(ListView):
    model = Forecast
    template_name = "city_detail.html"

    def get_context_data(self, **kwargs: Any):
        queryset = Forecast.objects.filter(city__slug=self.kwargs["slug"]).filter(
            datetime__gte=datetime.datetime.now(datetime.timezone.utc)
        )
        city = City.objects.get(slug=self.kwargs["slug"])
        tf = TimezoneFinder()
        # Dataset constructor for line chart
        tz = pytz.timezone(tf.timezone_at(lng=city.lon, lat=city.lat))
        time_city = datetime.datetime.now(tz=tz)
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
            "city_name": city.city_name,
            "forecast_list": queryset,
            "temp_trans": temp_trans,
            "time_city": time_city.strftime("%H:%M:%S"),
            "tz": str(tz),
        }
        return context

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        if self.request.htmx:
            city = City.objects.get(slug=self.kwargs["slug"])
            tf = TimezoneFinder()
            tz = pytz.timezone(tf.timezone_at(lng=city.lon, lat=city.lat))
            time_city = datetime.datetime.now(tz=tz)
            return render(
                self.request,
                "partials/time.html",
                {"time": time_city.strftime("%H:%M")},
            )
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        """
        Return a queryset which has at least 27 hours of forecast data in the future
        """
        queryset = self.model.objects.filter(city__slug=self.kwargs["slug"])
        if not queryset:
            get_weather_forecast(self.kwargs["slug"])
        # If not last forecast available is at least 27 hours in the future
        # Trigger API call to get new forecasts
        # Check: last forecast available is at least 27 hours in the future
        # Fail -> Http404
        min_future_date_forecast = datetime.datetime.now(
            datetime.timezone.utc
        ) + datetime.timedelta(hours=27)
        queryset = self.model.objects.filter(city__slug=self.kwargs["slug"])
        if min_future_date_forecast > getattr(queryset.latest("datetime"), "datetime"):
            get_weather_forecast(self.kwargs["pk"])
            queryset = self.model.objects.filter(city__slug=self.kwargs["slug"])
            if min_future_date_forecast > getattr(
                queryset.latest("datetime"), "datetime"
            ):
                raise Http404("No forecast data found")
        return self.model.objects.filter(city__slug=self.kwargs["slug"]).filter(
            datetime__gte=datetime.datetime.now(datetime.timezone.utc)
        )
