from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('materials/<str:cat>/', views.category_view, name='category'),
]
