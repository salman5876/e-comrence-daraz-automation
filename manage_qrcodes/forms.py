# manage_qrcodes/forms.py
from django import forms
from qrcodes.models import Game

class GameForm(forms.ModelForm):
    class Meta:
        model = Game
        fields = ['name', 'image']
