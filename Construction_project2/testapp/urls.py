
from django.urls import path
from testapp.views import *

urlpatterns = [
    path('home/',home,name='home'),
    path('add_product/',add_items),
    path('update_items/<int:id>/',update_items,name="update_items"),
]
