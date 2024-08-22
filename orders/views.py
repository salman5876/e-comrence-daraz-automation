from django.shortcuts import render
from .models import Order
from qrcodes.models import Game

def order(request):
    orders = Order.objects.all()
    games = Game.objects.all()
    games_with_images = [
        {'id': game.id, 'name': game.name, 'image_url': game.image.url}
        for game in games
    ]
    return render(request, 'orders_page.html', {'orders': orders, 'games': games_with_images})
