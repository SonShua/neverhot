from django.contrib import admin
from .models import City, Forecast

# Register your models here.

admin.site.register(City)


@admin.register(Forecast)
class ForecastAdmin(admin.ModelAdmin):
    list_display = ("get_city_name", "datetime", "dt_naive", "last_updated")
    ordering = ["city_id"]

    @admin.display(description="Name")
    def get_city_name(self, obj):
        return str(obj.city.city_name)
