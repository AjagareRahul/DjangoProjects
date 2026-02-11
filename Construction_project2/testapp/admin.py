from django.contrib import admin
from testapp.models import Material

# Register your models here.
class MaterialAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'image', 'description']

admin.site.register(Material, MaterialAdmin)
