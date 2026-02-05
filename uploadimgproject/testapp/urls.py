from django.urls import path
from .views import *

urlpatterns = [
    path('upload/', upload_img, name='upload'),
    path('show/', show_img, name='show'),
]
