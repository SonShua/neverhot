from typing import Any
from django.views.generic import ListView, CreateView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from weather.models import City
from weather.utils import get_locations
from django.shortcuts import render
from django.template.context_processors import csrf
from django.http import HttpRequest, HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_GET
from django.views.decorators.http import require_http_methods
from django.views.decorators.http import require_POST
from .forms import OddNumberForm, CityForm
from django.core.paginator import Paginator
from django.forms import formset_factory
from django.urls import reverse_lazy
from crispy_forms.utils import render_crispy_form
from crispy_forms.templatetags.crispy_forms_filters import as_crispy_field
import ratelimit


from django_htmx.middleware import HtmxDetails


class HtmxHttpRequest(HttpRequest):
    htmx: HtmxDetails


class AddCityView(FormView):
    form_class = CityForm
    template_name = "add_city.html"
    # success_url = reverse_lazy("search")

    def form_valid(self, form: Any) -> HttpResponse:
        if self.request.htmx:
            city_lists = get_locations(self.request, form.cleaned_data["city_name"])
            print(self.request.ratelimit)
            return render(
                self.request,
                "partials/partial_location_results.html",
                {
                    "city_created_list": city_lists[0],
                    "city_get_list": city_lists[1],
                    "nothing_found": city_lists[2],
                    "limit": city_lists[3],
                },
            )
        return super().form_valid(form)

    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            ctx = {}
            ctx.update(csrf(self.request))
            form_html = render_crispy_form(form, context=ctx)
            return self.form_invalid(form_html)


def check_locationname(request):
    """View function for dynamically validation checking of location name input.
    Could be integrated into SearchView (get method?)"""
    form = CityForm(request.GET)
    context = {
        "field": as_crispy_field(form["city_name"]),
        "valid": not form["city_name"].errors,  # If no errors, valid is set to True
    }
    return render(request, "partials/field.html", context)


class HomePageSearchView(ListView):
    model = City
    template_name = "home.html"

    def get_queryset(self):
        return self.model.objects.all()[:5]

    # @ratelimit.decorate(key="ip", rate="1/s")
    def get(self, request, *args, **kwargs):
        """The request has htmx appendix when the search bar is used. The client input is searched in the db and returned in page.object_list"""
        # if request.ratelimit["request_limit"] > 0:
        # reschedule with end of rate epoch
        #    print("request_waiting:" + request.ratelimit["end"])

        if request.htmx:
            search = request.GET.get("q")
            page_num = request.GET.get("page", 1)

            if search:
                citys = City.objects.filter(city_name__icontains=search)
            else:
                citys = City.objects.none()
            page = Paginator(object_list=citys.order_by("pk"), per_page=5).get_page(
                page_num
            )

            return render(
                request=request,
                template_name="partials/partial_results.html",
                context={"page": page},
            )
        return super().get(request, *args, **kwargs)


@ratelimit.decorate(key="ip", rate="1/m")
def rater(request):
    if request.htmx:
        request_limit = getattr(request.ratelimit, "request_limit")
        if request_limit == 0:
            search = request.GET.get("q")
        if request_limit == 1:
            search = "Please wait before making another call"
        print(f"{search}")
        return render(
            request=request,
            template_name="partial_rate.html",
            context={"search": search},
        )

    return render(request, "rate.html")


# Old function based search view, kept here for fragments
# def search(request):
#     if request.method == "GET":
#         context = {"form": CityForm()}
#         return render(request, "search.html", context)

#     elif request.method == "POST":
#         form = CityForm(request.POST)
#         if form.is_valid():
#             city_lists = get_locations(form.cleaned_data["city_name"])
#             return render(
#                 request,
#                 "partials/partial_location_results.html",
#                 {
#                     "city_created_list": city_lists[0],
#                     "city_get_list": city_lists[1],
#                     "nothing_found": city_lists[2],
#                     "limit": city_lists[3],
#                 },
#             )
#         ctx = {}
#         ctx.update(csrf(request))
#         form_html = render_crispy_form(form, context=ctx)
#         return HttpResponse(form_html)
