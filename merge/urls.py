from django.urls import path
from . import views
app_name = 'merge'

urlpatterns = [
    path('', views.merge, name='merge'),
    path('merge/', views.merge, name='merge_pdf'),
]
