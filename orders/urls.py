from django.urls import path
from .views import *

app_name = 'orders'
urlpatterns = [
    path('', order, name='orders'),
    # Other URL patterns for the orders app
]
