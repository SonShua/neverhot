from decimal import Decimal
from django.db.models import Q
import django_filters
from .models import City


class CityFilter(django_filters.FilterSet):
    query = django_filters.CharFilter(method="universal_search", label="")

    class Meta:
        model = City
        fields = ["query"]

    def universal_search(self, queryset, name, value):
        return City.objects.filter(
            Q(city_name__icontains=value) | Q(country__icontains=value)
        )
