from django.views.generic import ListView
from weather.models import City


class HomePageView(ListView):
    model = City
    template_name = "home.html"

    def get_queryset(self):
        return self.model.objects.all()
