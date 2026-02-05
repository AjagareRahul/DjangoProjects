from django.shortcuts import render
from .models import Student

def student_list(request):
    students = Student.objects.all()
   

def student_list(request):

    # 👉 Simple insert (only once)
    if Student.objects.count() == 2:
        Student.objects.create(name="Rahul", age=22, city="Pune")
        Student.objects.create(name="Amit", age=24, city="Mumbai")
        Student.objects.create(name="Neha", age=21, city="Nagpur")

    students = Student.objects.all()
    return render(request, 'testapp/home.html', {'students': students})
def addstudent(request):
    sname="Rani"
    sage=23
    scity="Bangalore"
    emp=Student(name=sname, age=sage, city=scity)
    emp.save()
    students = Student.objects.all()
    return render(request,'testapp/home.html',{'students': students})


