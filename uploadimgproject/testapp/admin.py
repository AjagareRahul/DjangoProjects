from django.contrib import admin
from testapp.models import  Image

# Register your models here.
class ImageAdmin(admin.ModelAdmin):
    list_display=('id','img')
admin.site.register(Image,ImageAdmin)