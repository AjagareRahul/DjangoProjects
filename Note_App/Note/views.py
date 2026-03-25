from django.shortcuts import render,redirect
from Note.models import Note
from Note.form import NoteForm
# Create your views here.

def home(request):
    notes=Note.objects.all()
    return render(request,'home.html',{'notes':notes})

def Form(request):
    form=NoteForm()
    # if request.mothod=='POST':  # OLD - typo: "mothod" should be "method"
    if request.method=='POST':
        form=NoteForm(request.POST)
        if form.is_valid():
            form.save()
            # return redirect('home')  # OLD - 'home' doesn't exist, URL name is 'name'
            return redirect('home')
    return render(request,'create.html',{'form':form})