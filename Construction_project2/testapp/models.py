from django.db import models

# Create your models here.
class Material(models.Model):
    name=models.CharField()
    price=models.IntegerField()
    image=models.ImageField(upload_to='media',blank=True,null=True)
    description=models.CharField()
    