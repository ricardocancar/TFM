# -*- coding: utf-8 -*-
from django import forms

from .models import Clasifications


class ClasificationsForm(forms.ModelForm):
    class Meta:
        model = Clasifications
        fields = [
                'video_name',
                'path',
                'label',
                'score'
                ]


class RawClasificationsForm(forms.Form):
    video_name = forms.CharField()
    path = forms.CharField()
    label = forms.CharField()
    score = forms.DecimalField()
