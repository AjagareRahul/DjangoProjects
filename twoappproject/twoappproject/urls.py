from django.contrib import admin
from django.urls import path
from app1 import views as v1
from app2 import views as v2

urlpatterns = [
    path('admin/', admin.site.urls),

    # app1 URLs
    path('about/', v1.app1),

    # app2 URLs
    path('home/', v2.app2),
]
