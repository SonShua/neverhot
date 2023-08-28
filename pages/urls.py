# pages/urls.py
from django.urls import path, include

from . import views

urlpatterns = [
    path("", views.HomePageSearchView.as_view(), name="home"),
    path("users/", include("django.contrib.auth.urls")),
    path("users/", include("users.urls")),
    path("weather/", include("weather.urls"), name="weather"),
    path("privacy_policy/", views.PrivacyView.as_view(), name="privacy"),
]
