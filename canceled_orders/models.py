from django.db import models
from django.utils import timezone

class CanceledOrder(models.Model):
    order_number = models.CharField(max_length=50)
    order_name = models.CharField(max_length=100)
    store_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    comment = models.TextField(blank=True, null=True)
    status = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.order_number
