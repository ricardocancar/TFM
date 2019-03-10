# -*- coding: utf-8 -*-
from django import forms

from .models import Resumen


class ResumenForm(forms.ModelForm):
    class Meta:
        model = Resumen
        fields = [
                'content',
                'numbers',
                ]


class RawResumenForm(forms.Form):
    content = forms.CharField()
    numbers = forms.DecimalField()
