from django.db import models

'''class Student(models.Model):
    name = models.CharField(max_length=30)
    age = models.IntegerField()
    marks = models.FloatField()'''

class Students(models.Model):
    name = models.CharField(max_length=30)
    rollno = models.IntegerField()
    email = models.EmailField()

    def __str__(self):
        return self.name

