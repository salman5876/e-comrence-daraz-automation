# manage_qrcodes/views.py
from django.shortcuts import render, get_object_or_404, redirect
from qrcodes.models import Game
from .forms import GameForm

def game_list(request):
    games = Game.objects.all()
    return render(request, 'manage_qrcodes/game_list.html', {'games': games})

# manage_qrcodes/views.py
def game_edit(request, pk):
    game = get_object_or_404(Game, pk=pk)
    if request.method == 'POST':
        form = GameForm(request.POST, request.FILES, instance=game)
        if form.is_valid():
            form.save()
            return redirect('manage_qrcodes:game_list')
    else:
        form = GameForm(instance=game)
    return render(request, 'manage_qrcodes/game_edit.html', {'form': form})

def game_delete(request, pk):
    game = get_object_or_404(Game, pk=pk)
    if request.method == 'POST':
        game.delete()
        return redirect('manage_qrcodes:game_list')
    return render(request, 'manage_qrcodes/game_confirm_delete.html', {'game': game})
