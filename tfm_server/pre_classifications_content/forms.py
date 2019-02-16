# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
from django import forms

from .models import PreClassificationsContent


class PreClassificationsContentForm(forms.ModelForm):
    class Meta:
        model = PreClassificationsContent
        fields = [
                'video_name',
                'start_end',
                'label',
                'text'
                ]


class RawPreClassificationsContentForm(forms.Form):
    video_name = forms.CharField()
    start_end = forms.CharField()
    label = forms.CharField()
    text = forms.CharField()
