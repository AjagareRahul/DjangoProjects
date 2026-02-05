from django.db import models

# Create your models here.
class Student(models.Model):
    name=models.CharField()
    rollno=models.IntegerField()
    marks=models.FloatField()
    

