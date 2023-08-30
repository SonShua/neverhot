from django import forms
from django.urls import reverse_lazy
from crispy_forms.helper import FormHelper, Layout
from crispy_forms.layout import Submit, Fieldset
from django.utils.translation import gettext_lazy as _


class InputForm(forms.Form):
    name = forms.CharField(max_length=200, help_text="Enter a city name of your choice")


class CityForm(forms.Form):
    class Meta:
        fields = ["city_name"]
        labels = {"city_name": "TEST"}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_id = "city-form"
        self.helper.add_input(Submit("submit", _("Search")))
        self.helper.attrs = {
            "hx-post": reverse_lazy("add_city"),
            "hx-target": "#results",
            "hx-swap": "innerHTML",
            "hx-indicator": "#ind",
        }
        # self.helper.layout = Layout(
        #     Fieldset(
        #         _("Which location are you missing {{user.username}}"),
        #         "city_name",
        #     ),
        #     self.helper.add_input(Submit("submit", "Search")),
        # )

    city_name = forms.CharField(
        label="",
        max_length=50,
        widget=forms.TextInput(
            attrs={
                "hx-get": reverse_lazy("check_locationname"),
                "hx-target": "#div_id_city_name",
                "hx-trigger": "keyup[target.value.length <= 4]",
                "placeholder": _("Location name"),
                "hx-indicator": "this",
            }
        ),
    )

    def clean_city_name(self):
        city_name = self.cleaned_data["city_name"]
        if len(city_name) <= 3:
            raise forms.ValidationError("Location name is too short")
        return city_name
