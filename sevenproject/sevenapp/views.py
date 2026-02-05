from django.http import HttpResponse

def first_view(request):
    return HttpResponse("Hello, this is the first view!")

def second_view(request):
    return HttpResponse("Hello, this is the second view!")

def third_view(request):
    return HttpResponse("Hello, this is the third view!")
