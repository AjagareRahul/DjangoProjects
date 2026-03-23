
from django.urls import path

#from django_inheritance.testapp.views import about
from .views import *

urlpatterns = [
    path('home/',home,name='home'),
    path('about/',about,name='about'),
    path('profile/',pro,name='pro'),    
]
    