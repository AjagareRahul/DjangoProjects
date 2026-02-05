from django.shortcuts import render,redirect
from testapp.models import Product
from .forms import Prod
def home(request):
    products = Product.objects.all()  
    return render(request, 'testapp/home.html', {'products': products})

def addprod(request):
    if request.method == 'POST':
        p = Prod(request.POST)
        if p.is_valid():
            name = p.cleaned_data['name']
            price = p.cleaned_data['price']
            description = p.cleaned_data['description']

            product = Product(name=name, price=price, description=description)
            product.save()
    else:
        p = Prod()

    products = Product.objects.all()
    return render(request, 'testapp/home.html', {'p': p, 'products': products})
def updateprod(request, pid):
    if request.method=='POST':
        name=request.POST['text1']
        price=request.POST['text2']
        description=request.POST['text3']   
        product=Product(name=name,price=price,description=description)
        product.save()
        
        return redirect('student/')
    else:
        prodform=Prod()
        product=Product.objects.get(id=pid)
        return render(request,'testapp/update.html',{'prodform':prodform,'product':product})