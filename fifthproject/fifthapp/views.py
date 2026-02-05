from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.
def home(request):
    return HttpResponse("Fifth App - Home Page")
def about(request):
    return HttpResponse("Fifth App - About Page")
def contact(request):
    return HttpResponse("Fifth App - Contact Page")
def services(request):
    return HttpResponse("Fifth App - Services Page")
def faq(request):
    return HttpResponse("Fifth App - FAQ Page")
