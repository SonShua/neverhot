from django import forms


class InputForm(forms.Form):
    city_name = forms.CharField(
        max_length=200, help_text="Enter a city name of your choice"
    )