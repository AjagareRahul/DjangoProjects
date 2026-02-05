from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.
def home(request):
    return HttpResponse("Welcome to the Seven1 App Home Page!")
def about(request):
    return HttpResponse("This is the About Page of the Seven1 App.")
def contact(request):
    return HttpResponse("Contact us at seven1app@example.com")