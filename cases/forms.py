from django import forms
from django.forms import ModelForm
from .models import CoronaCase

class CoronaCaseForm(ModelForm):
    class Meta:
        model = CoronaCase
        fields = ['case_type', 'num_cases', 'link', 'description']