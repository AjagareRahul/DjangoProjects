from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('materials/<str:cat>/', views.category_view, name='category'),
    path('add-item/', views.add_item, name='add_item'),
    path('buy/<int:id>/', views.buy_item, name='buy'),
]
