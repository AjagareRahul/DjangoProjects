from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.
def home(request):
    return HttpResponse("Sixth App - First Method")
def home(request):
    return HttpResponse("Sixth App -Second Method")
