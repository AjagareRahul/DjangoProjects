from django import forms
from moduleapp.models import Employee

class EmployeeForm(forms.Form):
    eno = forms.IntegerField(label='Employee Number')
    ename = forms.CharField(label='Employee Name', max_length=100)
    esal = forms.FloatField(label='Employee Salary')
