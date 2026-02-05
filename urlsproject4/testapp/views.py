from django.shortcuts import render
from testapp.forms import regform

# Create your views here.
def home_view(request):
    form=regform()
    return render(request, 'testapp/home.html',{'form':form})
