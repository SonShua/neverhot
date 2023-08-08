from django.views.generic import ListView
from weather.models import City
from weather.utils import get_locations
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django.views.decorators.http import require_GET
from django.views.decorators.http import require_http_methods
from django.views.decorators.http import require_POST
from .forms import OddNumberForm
from django.core.paginator import Paginator

from django_htmx.middleware import HtmxDetails


class HtmxHttpRequest(HttpRequest):
    htmx: HtmxDetails


# htmx


@require_GET
def csrf_demo(request: HtmxHttpRequest) -> HttpResponse:
    return render(request, "csrf-demo.html")


@require_POST
def csrf_demo_checker(request: HtmxHttpRequest) -> HttpResponse:
    form = OddNumberForm(request.POST)
    if form.is_valid():
        number = form.cleaned_data["number"]
        number_is_odd = number % 2 == 1
    else:
        number_is_odd = False
    return render(
        request,
        "csrf-demo-checker.html",
        {"form": form, "number_is_odd": number_is_odd},
    )


def SearchView(request):
    search = request.GET.get("q")

    if search:
        locations = get_locations(search)
    else:
        locations = City.objects.none()
    print(locations)
    return render(
        request=request,
        template_name="search.html",
        context={"locations_list": locations},
    )


class HomePageSearchView(ListView):
    model = City
    template_name = "home.html"

    def get_queryset(self):
        return self.model.objects.all()[:5]

    def get(self, request):
        if request.htmx:
            search = request.GET.get("q")
            page_num = request.GET.get("page", 1)

            if search:
                citys = City.objects.filter(city_name__icontains=search)
            else:
                citys = City.objects.none()
            page = Paginator(object_list=citys, per_page=5).get_page(page_num)

            return render(
                request=request,
                template_name="partial_results.html",
                context={"page": page},
            )
        return super().get(request)
