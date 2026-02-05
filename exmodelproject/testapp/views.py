from django.shortcuts import render
from testapp.models import Employee
# Create your views here.
def empdetails(request):
    emp=Employee.objects.all()
    return render(request, 'testapp/empinfo.html', {'emp': emp})
def addemp(request):
    ename="Bhanu"
    eid=1005
    dept="HR"
    emp=Employee(name=ename, empid=eid, dept=dept)
    emp.save()
    return render(request,'testapp/empinfo.html', {'emp': Employee.objects.all()})
