# -*- coding: utf-8 -*-
from django import forms

from .models import PoliticalClasification


class PoliticalClasificationForm(forms.ModelForm):
    class Meta:
        model = PoliticalClasification
        fields = [
                'political',
                'content',
                'numbers'
                ]


class RawPoliticalClasificationForm(forms.Form):
    political = forms.CharField()
    content = forms.CharField()
    numbers = forms.DecimalField()
