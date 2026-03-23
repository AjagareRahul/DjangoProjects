from django.db import models

# Create your models here.
class profile(models.Model):
    name=models.CharField(max_length=100)
    img=models.ImageField(upload_to='profilepics')
    resume=models.FileField(upload_to='resumes')
    def __str__(self):
        return self.name
    