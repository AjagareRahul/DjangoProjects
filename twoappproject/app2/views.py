from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
def app2(request):
    return HttpResponse("<h1>This is App 2</h1>")
