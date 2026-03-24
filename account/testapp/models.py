from django.db import models

# Create your models here.
class Recipe(models.Model):
    name=models.CharField(max_length=100)
    description=models.TextField()
    image=models.ImageField(upload_to='media', max_length=100)
    
    def __str__(self):
        return str(self.name)
    
