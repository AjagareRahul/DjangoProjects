from django.shortcuts import render , redirect
from testapp.models import Employee
from django.http import HttpResponseRedirect
# Create your views here.
def empinfo_view(request):
    employees = Employee.objects.all()
    return render(request,'testapp/empinfo.html', {'employees' : employees})

def form_view(request):
    employees = Employee.objects.all()
    return render(request,'testapp/forms1.html')

def addemp(request):
    if request.method=="POST":
        en=request.POST.get("txt1")
        enm = request.POST.get("txt2")
        esl = request.POST.get("txt3")

        emp=Employee(eno=en,ename=enm,esal=esl)             #for addemp
        emp.save()

        #emp = Employee(id=6,eno=en, ename=enm, esal=esl)      #for updating
        #emp.save()

        #emp=Employee(id=6)        #for delete
        #emp.delete()


    else:
        print("get request")

    return render(request,'testapp/Adddemp.html')

def show(request,my_id):
    #print(my_id)
    return render(request,'testapp/show.html', {'myid':my_id})

def home(request):
    return render(request, 'testapp/home.html')

def delview(request,id):
    e=Employee.objects.get(id=id)
    e.delete()
    return HttpResponseRedirect('/empinfo/')

def updateview(request,id):
    if request.method=="POST":
        en = request.POST.get("txt1")
        enm = request.POST.get("txt2")
        esl = request.POST.get("txt3")
        emp = Employee(id=id, eno=en, ename=enm, esal=esl)
        emp.save()
        return HttpResponseRedirect('/empinfo/')
    else:
        emp=Employee.objects.get(id=id)
    return render(request,'testapp/Updateemp.html',{'emp':emp})



