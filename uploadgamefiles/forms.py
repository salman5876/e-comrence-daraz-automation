# forms.py

from django import forms

class GameForm(forms.Form):
    game_name = forms.CharField(label='Game Name', max_length=100)
    game_size = forms.CharField(label='Game Size', max_length=100)
    # The `game_links` field will be a list of link values
    game_links = forms.CharField(label='Game Links', widget=forms.Textarea(attrs={'rows': 4}))
