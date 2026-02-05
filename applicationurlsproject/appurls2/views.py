
from django.http import HttpResponse

# Create your views here.
def home(request):
    return HttpResponse("<h>this is home page of appurls2</h>")
def about(request):
    return HttpResponse("<h>this is about page of appurls2</h>")