from django.contrib import admin
from accounts.models import Material

# Register your models here.
class MaterialAdmin(admin.ModelAdmin):
    list_display=['name','price','description','image']
admin.site.register(Material,MaterialAdmin)

