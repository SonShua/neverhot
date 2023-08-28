from typing import Any
from django.views.generic import ListView, CreateView, FormView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from weather.models import City
from weather.utils import get_locations
from django.shortcuts import render
from django.template.context_processors import csrf
from django.http import HttpRequest, HttpResponse
from .forms import CityForm
from django.core.paginator import Paginator
from crispy_forms.utils import render_crispy_form
from crispy_forms.templatetags.crispy_forms_filters import as_crispy_field


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
            page = Paginator(object_list=citys.order_by("pk"), per_page=5).get_page(
                page_num
            )

            return render(
                request=request,
                template_name="partials/partial_results.html",
                context={"page": page},
            )
        return super().get(request, *args, **kwargs)


class PrivacyView(TemplateView):
    # Shows the Privacy Policy
    template_name = "privacy.html"
