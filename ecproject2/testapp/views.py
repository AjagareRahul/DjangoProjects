from django.shortcuts import render
from testapp.models import Prductmodels
from testapp.forms import Add_product
# Create your views here.
def home(request):
    product=Prductmodels.objects.all()
    
    return render(request, 'testapp/home.html',{'product':product})
def add_product(request):
    if request.method=='POST':
        form=Add_product(request.POST)
        if form.is_valid():
            name=form.cleaned_data['name']
            price=form.cleaned_data['price']
            description=form.cleaned_data['description']
            
            form=Add_product(name=name,price=price,description=description)
            form.save()
    else:
        form=Add_product()
    return render(request,'testapp/home.html',{'form':form})