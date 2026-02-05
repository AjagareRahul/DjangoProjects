from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def first_view(request):
     return HttpResponse("<h1>Hello, this is the first view in testapp!</h1>")
def second_view(request):
     return HttpResponse("<h1>This is the second view in testapp!</h1>")
def third_view(request):
     return HttpResponse("<h1>Welcome to the third view in testapp!</h1>")