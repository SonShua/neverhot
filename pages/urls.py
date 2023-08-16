# pages/urls.py
from django.urls import path, include

from . import views

urlpatterns = [
    path("", views.HomePageSearchView.as_view(), name="home"),
    path("users/", include("django.contrib.auth.urls")),
    path("users/", include("users.urls")),
    path("weather/", include("weather.urls"), name="weather"),
    path("add_city/", views.AddCityView.as_view(), name="add_city"),
    path("check-locationname/", views.check_locationname, name="check_locationname"),
    path("rater", views.rater, name="rater"),
]
