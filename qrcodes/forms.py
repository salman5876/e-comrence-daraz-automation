# qrcodes/forms.py
from django import forms
from .models import Game

class SaveQRCodeForm(forms.ModelForm):
    class Meta:
        model = Game
        fields = ['name']
