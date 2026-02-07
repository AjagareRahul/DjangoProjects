from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Material
from .forms import MaterialForm

# DASHBOARD (PUBLIC)
def dashboard(request):
    return render(request, 'testapp/base.html')

# CATEGORY PAGE (cement, sand…)
def category_view(request, cat):
    items = Material.objects.filter(category=cat)
    return render(request, 'testapp/category.html', {
        'items': items,
        'cat': cat
    })

# ADD ITEM (LOGIN REQUIRED)
@login_required
def add_item(request):
    if request.method == 'POST':
        form = MaterialForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = MaterialForm()

    return render(request, 'testapp/add_item.html', {'form': form})

# BUY = ADD TO CART (for now simple)
@login_required
def buy_item(request, id):
    item = Material.objects.get(id=id)
    return render(request, 'testapp/buy.html', {'item': item})
