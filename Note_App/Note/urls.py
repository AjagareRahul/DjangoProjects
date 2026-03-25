from django.urls import path
from Note.views import *
urlpatterns = [
    path('',home,name='home'),
    path('create/',Form,name='Form')
]
