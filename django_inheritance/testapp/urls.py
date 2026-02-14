from django.urls import path
from testapp.views import *

urlpatterns = [
    path('', home, name='home'),          # http://127.0.0.1:8000/
    path('about/', about, name='about'),  # http://127.0.0.1:8000/about/
]
