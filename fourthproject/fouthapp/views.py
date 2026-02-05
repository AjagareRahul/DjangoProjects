from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
def home(request):
    return HttpResponse("Welcome to the Fourth App Home Page!")
def about(request):
    return HttpResponse("This is the About Page of the Fourth App.")
