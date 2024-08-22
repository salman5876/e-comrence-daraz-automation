# manage_qrcodes/urls.py
from django.urls import path
from . import views

app_name = 'manage_qrcodes'

urlpatterns = [
    path('', views.game_list, name='game_list'),
    path('edit/<int:pk>/', views.game_edit, name='game_edit'),
    path('delete/<int:pk>/', views.game_delete, name='game_delete'),
]
