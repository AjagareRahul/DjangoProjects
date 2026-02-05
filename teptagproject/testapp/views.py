from django.shortcuts import render
import datetime
# Create your views here.
def result(request):
    date=datetime.datetime.today()
    enm="Rahul Ajagare"
    esal=25000
    my_dict={'date':date,'ename':enm,'esal':esal}   

    return render(request, 'testapp/result2.html', my_dict)
def student(request):
    date=datetime.datetime.today()
    name="Rahul Ajagare"
    id=101
    marks=250
    my_dict={'date':date,'name':name,'id':id,'marks':marks}
    return render(request,'testapp/result3.html', my_dict)
    
    
    