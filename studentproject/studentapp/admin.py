from django.contrib import admin
from studentapp.models import Students

#class StudentAdmin(admin.ModelAdmin):
  #  list_display = ('id', 'name', 'age', 'marks')

#admin.site.register(Student, StudentAdmin)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('name', 'rollno', 'email')
admin.site.register(Students, EmployeeAdmin)