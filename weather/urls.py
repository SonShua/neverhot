from django.urls import path
from django.views.i18n import JavaScriptCatalog

from . import views

urlpatterns = [
    path("", views.CityView.as_view(), name="weather"),
    path("cities/<slug:slug>/", views.CityDetailView.as_view(), name="city_detail"),
    path("search/", views.CityHTMxTableView.as_view(), name="search"),
    path("check-locationname/", views.check_locationname, name="check_locationname"),
    path("add_city/", views.AddCityView.as_view(), name="add_city")
    # path("new/", CityAddView, name="city_new"),
    # path("city_select/", CitySelectView, name="city_select"),
    # path("no_city_found/", NoCityView, name="no_city_found"),
]
