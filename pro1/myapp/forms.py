from django import forms
from .models import Employee

class ContactForm(forms.Form):
    name=forms.CharField(max_length=100)
    email=forms.EmailField()
    message=forms.CharField(widget=forms.Textarea)
    
class EmployeeForm(forms.ModelForm):
    class Meta:
        model=Employee
        fields=['name','salary','city']