# pages/urls.py
from django.urls import path, include


from .views import HomePageView

urlpatterns = [
    path("", HomePageView.as_view(), name="home"),
    path("users/", include("django.contrib.auth.urls")),
    path("users/", include("users.urls")),
    path("weather/", include("weather.urls"), name="weather"),
]
