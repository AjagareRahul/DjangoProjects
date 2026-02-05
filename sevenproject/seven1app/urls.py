from django.urls import path
from seven1app.views import *

urlpatterns = [
    path('home/', home),
    path('about/', about),
    path('contact/', contact),
]
