from django.urls import path
from . import views
app_name = 'gamelist'

urlpatterns = [
    path('', views.gamelist, name='gamelist'),

]
