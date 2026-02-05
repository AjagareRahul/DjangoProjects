from django.shortcuts import render
from .forms import SampleForm
from testapp.models import Employee

# Create your views here.
def show_forms(request):
    if request.method == 'POST':
        form = SampleForm(request.POST)
        if form.is_valid():
            name=form.cleaned_data['name']
            email=form.cleaned_data['email']
            emp = Employee(ename=name, email=email)
            emp.save()
            print(f"Name: {name}, Email: {email}")
#return render(request, 'testapp/register.html')
            # Process the data in form.cleaned_data as required
            # For example, save it to the database
    else:   
            return render(request, 'testapp/register.html')
    form = SampleForm()
    return render(request, 'testapp/register.html', {'form': form}) 

    