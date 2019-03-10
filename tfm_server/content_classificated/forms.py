# -*- coding: utf-8 -*-
from django import forms

from .models import ClasificationsContent


class ClasificationsContentForm(forms.ModelForm):
    class Meta:
        model = ClasificationsContent
        fields = [
                'video_name',
                'start_end',
                'label',
                'text',
                'tag',
                'human_term',
                'others_tags',
                ]


class RawClasificationsContentForm(forms.Form):
    video_name = forms.CharField()
    start_end = forms.CharField()
    label = forms.CharField()
    text = forms.CharField()
    tag = forms.CharField()
    human_term = forms.CharField()
    others_tags = forms.CharField()


