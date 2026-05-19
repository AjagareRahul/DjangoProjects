from django.db import models

# Create your models here.
class Student(models.Model):
    name=models.CharField(max_length=100)
    age=models.IntegerField()
    
    def __str__(self):
        return self.name

class Product(models.Model):
    name=models.CharField(max_length=100)
    price=models.IntegerField()
    
class Employee(models.Model):
    name=models.CharField(max_length=100)
    salary=models.IntegerField()
    city=models.CharField(max_length=100)
    