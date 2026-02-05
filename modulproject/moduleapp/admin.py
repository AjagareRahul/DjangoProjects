from django.contrib import admin
from moduleapp.models import Employee

class EmployeeAdmin(admin.ModelAdmin):
    list_display = ['eno', 'ename', 'esal']

admin.site.register(Employee, EmployeeAdmin)