from django.shortcuts import render, redirect, get_object_or_404
from testapp.models import Recipe
from django.contrib import messages

# Create your views here.

def home(request):
     rec=Recipe.objects.all()
     return render(request,'base.html',{'rec':rec})

def recipe_details(request,pk):
     rec=get_object_or_404(Recipe,pk=pk)
     return render(request,'recipe_details.html',{'rec':rec})
def create(request):
     if request.method=='POST':
          name=request.POST.get('name')
          description=request.POST.get('description')
          image=request.FILES.get('image')
          recipe=Recipe.objects.create(
               name=name,
               description=description,
               image=image
          )
          messages.success(request,'Recipe created successfully')
          return redirect('recipe_detail', pk=recipe.id)
     return render(request,'base.html')
def update(request, id):
    rec = get_object_or_404(Recipe, pk=id)
    if request.method == 'POST':
        rec.name = request.POST.get('name')
        rec.description = request.POST.get('description')
        if request.FILES.get('image'):
            rec.image = request.FILES.get('image')
        rec.save()
        messages.success(request, 'Recipe updated successfully')
        return redirect('recipe_detail', pk=rec.id)
    return render(request, 'update.html', {'rec': rec})

def delete(request, id):
    rec = get_object_or_404(Recipe, pk=id)
    rec.delete()
    messages.success(request, 'Recipe deleted successfully')
    return redirect('home')