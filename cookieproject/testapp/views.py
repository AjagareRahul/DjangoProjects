from django.shortcuts import render
from datetime import datetime, timedelta
from django.utils import timezone
# Create your views here.
def setcookie(request):
    response=render(request,'testapp/setcookie.html')
    response.set_cookie('name',value='Rajeev',expires=datetime.utcnow()+timedelta(days=2))
    #response.set_cookie('name',value='Rahul',expires=timezone.now()+timedelta(days=2))
    return response

def readcookie(request):
    name=request.COOKIES.get('name','Rahul')
    return render(request,'testapp/readcookie.html',{'name':name})

def delcookie(request):
    response=render(request,'testapp/delcookies.html')
    response.delete_cookie('name')
    return response