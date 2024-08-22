# qrcode_generator/forms.py
from django import forms
from qrcodes.models import Game

class QRCodeForm(forms.Form):
    file_link = forms.URLField(label='File Link', max_length=200)
    file_name = forms.CharField(label='File Name', max_length=100)

class SaveQRCodeForm(forms.ModelForm):
    class Meta:
        model = Game
        fields = ['name']
