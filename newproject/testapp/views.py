from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.
def example_view(request):
    return HttpResponse('<h1>This is an example view response.</h1>')
def another_view(request):
    return HttpResponse('<h1>This is another view response.</h1>')
def addition(request,a,b):
    c=a+b
    return HttpResponse(f'The addition of {a} and {b} is {c}' )