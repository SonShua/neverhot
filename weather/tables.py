import django_tables2 as tables
from .models import City


class CityHTMxTable(tables.Table):
    country = tables.Column(verbose_name="Country")
    lat = tables.Column(verbose_name="Latitude")
    lon = tables.Column(verbose_name="Longitude")
    city_name = tables.RelatedLinkColumn(verbose_name="Name")

    class Meta:
        model = City
        template_name = "tables/bootstrap_htmx.html"
        fields = ("city_name", "country", "lat", "lon")
