from django.db import models

class Material(models.Model):
    name = models.CharField(max_length=100)
    price = models.FloatField()
    description = models.TextField()
    image = models.ImageField(upload_to='materials/', blank=True, null=True)

    def __str__(self):
        return self.name
