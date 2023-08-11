# pages/urls.py
from django.urls import path, include


from .views import HomePageSearchView, search, check_locationname

from . import views

urlpatterns = [
    path("", HomePageSearchView.as_view(), name="home"),
    path("users/", include("django.contrib.auth.urls")),
    path("users/", include("users.urls")),
    path("weather/", include("weather.urls"), name="weather"),
    path("search/", search, name="search"),
    path("check-locationname/", check_locationname, name="check_locationname"),
]
