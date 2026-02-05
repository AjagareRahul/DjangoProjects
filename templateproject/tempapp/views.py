from django.shortcuts import render
def result(request):
    return render(request, 'testapp/index.html')
def result1(request):
    return render(request, 'testapp/about.html')

# Create your views here.
   # return render(request, 'testapp/index.html')    