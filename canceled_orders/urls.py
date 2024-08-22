from django.urls import path
from .views import *
app_name = 'canceled_orders'
urlpatterns = [
    path('', canceled_orders, name='canceled_orders'),
    path('canceled_orders/', canceled_orders, name='canceled_orders'),
    path('edit/<int:pk>/', edit_order, name='edit_order'),
    path('delete/<int:pk>/', CanceledOrderDeleteView.as_view(), name='delete_order'),
]
