from django import forms
from testapp.models import Product
class Prod(forms.Form):
    name=forms.CharField()
    price=forms.FloatField()
    description=forms.CharField()
    