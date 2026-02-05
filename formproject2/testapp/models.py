from django.db import models

# Create your models here.

class Employee(models.Model):
    ename = models.CharField(max_length=100)
    email=models.EmailField('type=email')
    def __str__(self):
        return self.ename
    
