from django.db import models

# Create your models here.
class Material(models.Model):
    CATEGORY = [
        ('cement', 'Cement'),
        ('sand', 'Sand'),
        ('steel', 'Steel'),
        ('bricks', 'Bricks'),
        ('pipes', 'Steel Pipes'),
    ]

    name = models.CharField(max_length=100)
    category = models.CharField(max_length=20, choices=CATEGORY)
    price = models.IntegerField()
    description = models.TextField()
    image = models.ImageField(upload_to='materials/')

    def __str__(self):
        return self.name
