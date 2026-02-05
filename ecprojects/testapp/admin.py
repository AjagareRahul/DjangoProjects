from django.contrib import admin
from testapp.models import Product

# Register your models here.
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'description')
admin.site.register(Product, ProductAdmin)