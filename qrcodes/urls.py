from django.urls import path
from . import views

app_name = 'qrcodes'

urlpatterns = [
    path('', views.upload_qr_codes, name='upload_qr_codes'),
    # Remove the redundant path declaration
]
