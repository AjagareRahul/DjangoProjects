from django.shortcuts import render,redirect
from studentapp.forms import StudentForm
from studentapp.models import Students
from django.http import  HttpResponseRedirect  
def Student(request):
    students = Students.objects.all()
    return render(request, 'testapp/studentinfo.html', {'students': students})


def addemp(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            rollno = form.cleaned_data['rollno']
            email = form.cleaned_data['email']

            emp = Students(name=name, rollno=rollno, email=email)
            emp.save()

           # form = StudentForm()  # Clear the form after saving 
    else:
        form = StudentForm()

    return render(request, 'testapp/addemp.html', {'form': form})
def update(request, sid):
    student = Students.objects.get(id=sid)   

    if request.method == 'POST':
        student.name = request.POST.get('text1')
        student.rollno = request.POST.get('text2')
        student.email = request.POST.get('text3')
        student.save()

        return redirect('/student/')

    return render(request, 'testapp/updatestd.html', {'student': student})
def deletes(request, sid):
    s = Students.objects.get(id=sid)
    s.delete()
    return redirect('/student/')

'''def addstd(request):
    snm="Sandeep"
    ag=15
    mrks=85
    std=Student(name=snm, age=ag, marks=mrks)
    std.save()
    return HttpResponse("Student added successfully")
def updatestd(request,myid):
    snm="Sandeep Kumar"
    std=Student.objects.get(id=myid)
    std.name=snm
    std.save()
    return HttpResponse("Student updated successfully")
def deletestd(request,myid):
    std=Student.objects.get(id=myid)
    std.delete()
    return HttpResponse("Student deleted successfully")'''

