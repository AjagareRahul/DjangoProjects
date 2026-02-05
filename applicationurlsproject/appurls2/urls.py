from django.urls import path
from appurls2 import views

urlpatterns = [
    path('home1/', views.home),
    path('about1/', views.about),
]

