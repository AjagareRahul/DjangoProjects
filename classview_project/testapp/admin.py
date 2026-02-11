from django.contrib import admin
from testapp.models import Employee

# Register your models here.
class formAdmin(admin.ModelAdmin):
    list_display=['name','email']
admin.site.register(Employee,formAdmin)