from django import forms
from testapp.models import Prductmodels

class Add_product(forms.ModelForm):
    name=forms.CharField()
    price=forms.FloatField()
    description=forms.CharField()
