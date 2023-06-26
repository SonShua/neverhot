from django.urls import path

from .views import CityView

urlpatterns = [
    path("", CityView.as_view(), name="weather"),
]
