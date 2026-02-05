from django.shortcuts import render

# Create your views here.
def home_view(request):
    return render(request, 'testapp/home.html')

def emprecords(request,myid):
    return render(request, 'testapp/emprecords.html', {'mid': myid})