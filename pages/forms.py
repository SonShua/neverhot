from __future__ import annotations

from django import forms
from django.urls import reverse_lazy
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Submit


class CityForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_id = "city-form"
        self.helper.attrs = {
            "hx-post": reverse_lazy("add_city"),
            "hx-target": "#results",  # div where the POST results are displayed
            "hx-swap": "innerHTML",  # inner swap so the POST is repeatable
            "hx-indicator": "#spinner",  # display the spinner waiting for response
        }
        self.helper.layout = Layout(
            Fieldset(
                "Which location are you missing {{user.username}}",
                "city_name",
            ),
            self.helper.add_input(Submit("submit", "Search")),
        )

    city_name = forms.CharField(
        max_length=50,
        widget=forms.TextInput(
            attrs={
                "hx-get": reverse_lazy("check_locationname"),
                "hx-target": "#div_id_city_name",
                "hx-trigger": "keyup[target.value.length > 3]",
            }
        ),
    )

    def clean_city_name(self):
        city_name = self.cleaned_data["city_name"]
        if len(city_name) <= 3:
            raise forms.ValidationError("Location name is too short")
        return city_name
