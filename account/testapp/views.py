from django.shortcuts import render
from testapp.models import *
# Create your views here.

def home(request):
    rec=Recipe.objects.all()
    return render(request,'base.html', {'rec':rec})