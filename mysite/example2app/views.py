from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.
def home(request):
    return render(request, 'example2app/home.html')
def about(request):
    return HttpResponse("This is the about page of Example2App.")       
def contact(request):
    return HttpResponse("This is the contact page of Example2App.")
def services(request):
    return HttpResponse("This is the services page of Example2App.")
