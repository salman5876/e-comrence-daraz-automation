from django.urls import path
from . import views

app_name = 'uploadgamefiles'

urlpatterns = [
    path('', views.uploadgamefiles, name='uploadgamefiles'),
    # Remove the redundant path declarationz
    path('upload/', views.uploadgamefiles, name='uploadgamefiles'),
]
