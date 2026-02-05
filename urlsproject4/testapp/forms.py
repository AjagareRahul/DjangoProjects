from django import forms

class regform(forms.Form):
    name = forms.CharField()
    email = forms.EmailField()
