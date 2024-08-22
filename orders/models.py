# orders/models.py

from django.db import models

class Order(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

# class Game(models.Model):
#     name = models.CharField(max_length=100)
#     image = models.ImageField(upload_to='games/images/')

#     def __str__(self):
#         return self.name
