from django.urls import path
from django.views.i18n import JavaScriptCatalog

from .views import (
    CityView,
    CityDetailView,
    CityHTMxTableView,
)  # , CityAddView  # CitySelectView, NoCityView

urlpatterns = [
    path("", CityView.as_view(), name="weather"),
    path("<int:pk>/", CityDetailView.as_view(), name="city_detail"),
    path("table/", CityHTMxTableView.as_view(), name="table")
    # path("new/", CityAddView, name="city_new"),
    # path("city_select/", CitySelectView, name="city_select"),
    # path("no_city_found/", NoCityView, name="no_city_found"),
]
