from django.shortcuts import render,redirect
from django.http import HttpResponse
from myapp.models import Employee
from .forms import ContactForm,EmployeeForm

# Create your views here.

def home(request):
    employee=Employee.objects.all()
    
    return render(request,'home.html',{'Employee':employee})
    
    
    ''' data={
        'name':'Danny',
        'age':22
    }
    data2={
        'name':'Rajeev',
        'city':'Pune',
        'profession':'Developer'
    }
    data.update(data2)'''

    #return render(request,'home.html')
    #return HttpResponse('This is Home Page')


def add_employee(request):
    if request.method=="POST":
        name=request.POST.get('name')
        salary=request.POST.get('salary')
        city=request.POST.get('city')
        
        Employee.objects.create(
            name=name,
            salary=salary,
            city=city,
        )
        print(name,salary,city)

        return redirect('home')
    return render(request,'add_employee.html')


def edit_employee(request,id):
    emp=Employee.objects.get(id=id)
    
    if request.method=="POST":
        emp.name=request.POST.get('name')
        emp.salary=request.POST.get('salary')
        emp.city=request.POST.get('city')
        emp.save()
        
        return redirec('home')
    
    return render(request,'edit_employee.html',{'emp':emp})



def delete(request,id):
    emp=Employee.objects.get(id=id)
    emp.delete()
    
    return redirect('home')

def about(request):
    data2 = {
        'skills':['python','Django','sql']
        
    }
    return render(request,'about.html',data2)

    ''' data= {
        'title':'About Us',
        'description':'This is my first Django project'
    }'''
   
    
    #data.update(data2)

def contact(request):
    return HttpResponse('This is Contact Page')

def Contact(request):
    form=ContactForm()
    
    if request.method=="POST":
        form=ContactForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
    return render(request,'contact.html',{'form':form})

def add_employeee(request):
    form=EmployeeForm()
    
    if request.method=="POST":
        form=EmployeeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
            
    return render(request,'add_employees.html',{'form':form})