from django.shortcuts import render
from testapp.models import Student

# Create your views here.
def home_view(request):
    return render(request, 'testapp/addstudent.html')
def student_view(request):
    students=Student.objects.all()
    return render(request, 'testapp/student.html', {'students':students})  
def add_student(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        rollno = request.POST.get('rollno')
        marks = request.POST.get('marks')
        student = Student(name=name, rollno=rollno, marks=marks)
        student.save()
    return render(request, 'testapp/add_student.html') 
