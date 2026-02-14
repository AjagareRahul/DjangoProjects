#from django.contrib import admin
from django.urls import path
from testapp.views import *
urlpatterns = [
    #path('admin/', admin.site.urls),
    path('getemp/',get_employee),
    path('home/',lIST_Employee.as_view()),
    path('Details/<id>/',Details.as_view())
    
]
