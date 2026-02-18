"""
URL configuration for rahulsite project.
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from rahulsapp.views import home

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
]

# Serve static files in development
if settings.DEBUG:
    if settings.STATICFILES_DIRS:
        urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
