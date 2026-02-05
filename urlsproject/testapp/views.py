from django.shortcuts import render


# Create your views here.
def home(request):
    return render(request, 'testapp/home.html')

def emprecords(request,myid):
    return render(request, 'testapp/emprecords.html', {'mid': myid})