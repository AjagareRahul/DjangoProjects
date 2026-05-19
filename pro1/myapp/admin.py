from django.contrib import admin
from myapp.models import * # Student,Employee,Product

# Register your models here.
admin.site.register(Student)
admin.site.register(Employee)
admin.site.register(Product)
