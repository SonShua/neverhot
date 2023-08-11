from django.views.generic import ListView, CreateView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from weather.models import City
from weather.utils import get_locations
from django.shortcuts import render
from django.template.context_processors import csrf
from django.http import HttpRequest, HttpResponse
from django.views.decorators.http import require_GET
from django.views.decorators.http import require_http_methods
from django.views.decorators.http import require_POST
from .forms import OddNumberForm, CityForm
from django.core.paginator import Paginator
from django.forms import formset_factory
from crispy_forms.utils import render_crispy_form
from crispy_forms.templatetags.crispy_forms_filters import as_crispy_field

from django_htmx.middleware import HtmxDetails


class HtmxHttpRequest(HttpRequest):
    htmx: HtmxDetails


def search(request):
    if request.method == "GET":
        context = {"form": CityForm()}
        return render(request, "search.html", context)

    elif request.method == "POST":
        form = CityForm(request.POST)
        ctx = {}
        if form.is_valid():
            city_list = get_locations(form.cleaned_data["city_name"])
            # ctx = {"city_list": city_list}
        ctx.update(csrf(request))
        form_html = render_crispy_form(form, context=ctx)
        return render(
            request,
            "partial_location_results.html",
            {"form": form_html, "city_list": city_list},
        )


def check_locationname(request):
    form = CityForm(request.GET)
    context = {
        "field": as_crispy_field(form["city_name"]),
        "valid": not form["city_name"].errors,
    }
    return render(request, "partials/field.html", context)


class HomePageSearchView(ListView):
    model = City
    template_name = "home.html"

    def get_queryset(self):
        return self.model.objects.all()[:5]

    def get(self, request, *args, **kwargs):
        """The request has htmx appendix when the search bar is used. The client input is searched in the db and returned in page.object_list"""
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
        return super().get(request, *args, **kwargs)
