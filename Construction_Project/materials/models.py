from django.db import models

class Material(models.Model):
    CATEGORY_CHOICES = [
        ('cement', 'Cement'),
        ('sand', 'Sand'),
        ('steel', 'Steel'),
        ('bricks', 'Bricks'),
        ('pipes', 'Steel Pipes'),
    ]

    name = models.CharField(max_length=100)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    price = models.IntegerField()
    description = models.TextField()
    image = models.ImageField(upload_to='materials/')

    def __str__(self):
        return self.name
