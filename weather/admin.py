from django.contrib import admin
from .models import City, Forecast

# Register your models here.


class ForecastInline(admin.TabularInline):
    model = Forecast
    fields = ["datetime", "dt_naive"]


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ("city_name", "last_updated")
    ordering = ["id"]
    inlines = [
        ForecastInline,
    ]


@admin.register(Forecast)
class ForecastAdmin(admin.ModelAdmin):
    list_display = ("get_city_name", "datetime", "dt_naive", "last_updated")
    ordering = ["city_id"]

    @admin.display(description="Name")
    def get_city_name(self, obj):
        return str(obj.city.city_name)
