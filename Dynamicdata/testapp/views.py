from django.shortcuts import render
from .models import profile 

# Create your views here.
def home(request):
    data = {
        'name':'sai',
        'age':22,
        'city':'hyd'
    }
    return render(request, 'home.html', data)

def about(request):
    return render(request, 'about.html')    

def pro(request):
    profiledata=profile.objects.all()
    return render(request, 'profile.html',{'profiledata':profiledata})
