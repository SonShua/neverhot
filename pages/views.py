from django.views.generic import ListView, TemplateView
from weather.models import City


class HomePageView(ListView):
    model = City
    template_name = "home.html"

    def get_queryset(self):
        return self.model.objects.all()


class DemoView(TemplateView):
    template_name = "demo.html"
