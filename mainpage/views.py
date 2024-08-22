from django.shortcuts import render

from qrcodes.models import Game

def mainpage(request):
    return render(request, 'main.html')
