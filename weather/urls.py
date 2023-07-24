from django.urls import path

from .views import (
    CityView,
    CityDetailView,
    sample_bar_chart,
    forecasty,
)  # , CityAddView  # CitySelectView, NoCityView

urlpatterns = [
    path("", CityView.as_view(), name="weather"),
    path("<int:pk>/", CityDetailView.as_view(), name="city_detail"),
    path("chart/", sample_bar_chart, name="sampling"),
    path("json/", forecasty, name="data_forecast")
    # path("new/", CityAddView, name="city_new"),
    # path("city_select/", CitySelectView, name="city_select"),
    # path("no_city_found/", NoCityView, name="no_city_found"),
]
