# pages/urls.py
from django.urls import path, include

from .views import HomePageView

urlpatterns = [
    path("", HomePageView.as_view(), name="home"),
    path("weather/", include("weather.urls"), name="weather"),
]
