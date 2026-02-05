from django.urls import path
from testapp import views

urlpatterns = [
    path('', views.example_view, name='example'),
    path('another/', views.another_view, name='another'),
    path('add/<int:a>/<int:b>/', views.addition, name='addition'),
]
