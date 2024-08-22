
from django.db import models

class Game(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='qrcodes/')

    class Meta:
        ordering = ['name']
