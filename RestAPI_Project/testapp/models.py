from django.db import models

# Create your models here.
class Employee(models.Model):
    name=models.CharField()
    salary=models.FloatField()
    def __str__(self):
        return self.name