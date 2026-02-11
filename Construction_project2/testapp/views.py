from django.shortcuts import render, redirect
from django.shortcuts import render, redirect, get_object_or_404
from testapp.models import Material
from testapp.forms import MaterialForm

def home(request):
    items = Material.objects.all()
    return render(request, 'home.html', {'item': items})

def add_items(request):
   if request.method == "POST":
      form = MaterialForm(request.POST,request.FILES)
      if form.is_valid():
         form.save()
         return redirect('home')   # redirect after POST
   else:
        form = MaterialForm()
        
   items = Material.objects.all()
   return render(request, 'home.html', {'m': form, 'i': items})

def update_items(request, id):
    material = get_object_or_404(Material, id=id)

    if request.method == "POST":
        form = MaterialForm(request.POST, instance=material)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = MaterialForm(instance=material)

    return render(request, 'update_items.html', {'form': form, 'material': material})
      
      