from django.contrib import admin
from .models import CanceledOrder

@admin.register(CanceledOrder)
class CanceledOrderAdmin(admin.ModelAdmin):
    list_display = ('order_number', 'order_name', 'store_name', 'phone_number', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('order_number', 'order_name', 'store_name', 'phone_number')
