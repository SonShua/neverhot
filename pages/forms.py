from __future__ import annotations

from django import forms


class OddNumberForm(forms.Form):
    number = forms.IntegerField()


class CityNameForm(forms.Form):
    city_name = forms.CharField(max_length=100)
