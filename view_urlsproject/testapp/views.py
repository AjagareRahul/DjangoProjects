from django.shortcuts import render
from django.http import HttpResponse
import datetime


# Create your views here.
def home_view(request):
    return render(request,'testapp/results.html')
def time_view(request):
    current_datetime = datetime.datetime.now()
    name="User"
    sname="Tester"
    age=25
    my_dict={'datetime':current_datetime,'name':name,'sname':sname,'age':age}
    return render(request,'testapp/results.html',context=my_dict)