from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def home(request):
    return HttpResponse("Welcome to App 1 Home Page")
def about(request):
    return HttpResponse("This is the About Page of App 1")

