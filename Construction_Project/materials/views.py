from django.shortcuts import render
from .models import Material

def dashboard(request):
    return render(request, 'testapp/home.html')

def category_view(request, cat):
    items = Material.objects.filter(category=cat)
    return render(request, 'testapp/category.html', {'items': items, 'cat': cat})
