# qrcode_generator/urls.py
from django.urls import path
from .views import generate_qr, download_qr, save_qr_to_db

app_name = 'qrcode_generator'

urlpatterns = [
    path('', generate_qr, name='generate_qr'),
    path('download_qr/', download_qr, name='download_qr'),
    path('save_qr_to_db/', save_qr_to_db, name='save_qr_to_db'),
]
