from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Category(models.Model):
    name=models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
class Post(models.Model):
    title=models.CharField(max_length=200)
    content=models.TextField()
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    category=models.ForeignKey(Category,on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Comment(models.Model):
    post=models.ForeignKey(Post,on_delete=models.CASCADE)
    text=models.TextField()

    def __str__(self):
        return self.text[:50]