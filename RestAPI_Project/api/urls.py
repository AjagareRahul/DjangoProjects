#from django.contrib import admin
from django.urls import path
from testapp.views import *
urlpatterns = [
    #path('admin/', admin.site.urls),
    path('getemp/',get_employee),
]
