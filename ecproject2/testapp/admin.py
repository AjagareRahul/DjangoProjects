from django.contrib import admin
from .models import Prductmodels

class ProductAdmin(admin.ModelAdmin):
    list_display=('name','price','description')
admin.site.register(Prductmodels,ProductAdmin)