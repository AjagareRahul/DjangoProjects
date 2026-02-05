from django.shortcuts import render,redirect
from moduleapp.models import Employee
from moduleapp.forms import EmployeeForm  

def employee(request): 
    employees = Employee.objects.all()
    return render(request, 'testapp/empinfo.html', {'employees': employees})

def addemp(request):
    if request.method == 'POST':
        form = EmployeeForm(request.POST) 
        if form.is_valid():
            eno = form.cleaned_data['eno']
            ename = form.cleaned_data['ename']
            esal = form.cleaned_data['esal']

            emp = Employee(eno=eno, ename=ename, esal=esal)
            emp.save()
    else:
        form = EmployeeForm()

    return render(request, 'testapp/addemp.html', {'form': form})
def updateemp(request,eid):
    if request.method=='POST':
        eno = request.POST.get('text1')
        ename = request.POST.get('text2')
        esal = request.POST.get('text3')
        emp=Employee(id=eid, eno=eno, ename=ename, esal=esal)
        emp.save()
        return redirect('/employee/')
    else:
        empfrm=EmployeeForm()
        emp=Employee.objects.get(id=eid)
        return render(request,'testapp/updateemp.html',{'empfrm':empfrm,'emp':emp})
def deletes(request,eid):
    e=Employee.objects.get(id=eid)
    e.delete()
    return redirect('/employee/')




#without using forms.py
'''def addemp(request):
    en=6
    enm="Rahul"
    esl=45000
    emp=Employee(eno=en, ename=enm, esal=esl)
    emp.save()
    return HttpResponse("Employee added successfully")
def updateemp(request,myid):
    en=3
    enm="Ravi"
    esl=10000
    emp=Employee(id=myid,eno=en, ename=enm, esal=esl)
    emp.save()
    return HttpResponse("Employee updated successfully")
def deletes(request,myid):
    e=Employee.objects.get(id=myid)
    e.delete()
    return HttpResponse("Employee deleted successfully")'''


