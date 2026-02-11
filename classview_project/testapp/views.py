from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from testapp.models import Employee
from testapp.form import SampleForm


class Classview(View):
    def get(self, request):
        return HttpResponse("Welcome to class view")


class Templatesview(View):
    def get(self, request):
        form = SampleForm()
        return render(request, 'home.html', {'form': form})


class ClassForm(View):
    def get(self, request):
        form = SampleForm()
        return render(request, 'home.html', {'form': form})

    def post(self, request):
        form = SampleForm(request.POST)

        if form.is_valid():
            name = form.cleaned_data.get('name')
            email = form.cleaned_data.get('email')

            print("Name:",name,"Email:", email)
            return HttpResponse("Form Submitted")

        return render(request, 'home.html', {'form': form})


class show(View):
    def get(self, request):
        e = Employee.objects.all()
        return render(request, 'home.html', {'e': e})
