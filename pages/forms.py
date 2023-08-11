from __future__ import annotations

from django import forms
from django.urls import reverse_lazy
from django.core.validators import RegexValidator
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit


class OddNumberForm(forms.Form):
    number = forms.IntegerField()


class CityForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_id = "city-form"
        self.helper.add_input(Submit("submit", "Submit"))
        self.helper.attrs = {
            "hx-post": reverse_lazy("search"),
            # Target is the HTML element that is to be swapped
            "hx-target": "#results",
            # OuterHTML swap would swap out the target section, producing a target error after first POST
            "hx-swap": "innerHTML",
            # Activates the div id spinner while data is being fetched
            "hx-indicator": "#spinner",
        }

    city_name = forms.CharField(
        max_length=50,
        widget=forms.TextInput(
            attrs={
                # Dynamic GET of user input and validation on the go
                "hx-get": reverse_lazy("check_locationname"),
                "hx-target": "#div_id_city_name",
                "hx-trigger": "keyup[target.value.length > 2]",
            }
        ),
    )

    def clean_city_name(self):
        city_name = self.cleaned_data["city_name"]
        if len(city_name) <= 3:
            raise forms.ValidationError("Location name is too short")
        return city_name
