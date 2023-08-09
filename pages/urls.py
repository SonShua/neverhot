# pages/urls.py
from django.urls import path, include


from .views import (
    csrf_demo,
    csrf_demo_checker,
    HomePageSearchView,
)

urlpatterns = [
    path("", HomePageSearchView.as_view(), name="home"),
    path("users/", include("django.contrib.auth.urls")),
    path("users/", include("users.urls")),
    path("weather/", include("weather.urls"), name="weather"),
    path("csrf-demo/", csrf_demo),
    path("csrf-demo/checker/", csrf_demo_checker),
]
