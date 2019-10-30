from django.shortcuts import render
from django.http import HttpResponse
from .my_scrabble.game import ScrabbleBoard

def index(request):
    board = ScrabbleBoard.Board()
    grid = board.grid

    context = {'grid':grid}

    return render(request, "scrabble/scrabble_view.html", context)
# Create your views here.

def clicksquare(request):
    return HttpResponse("click")

def display_id(request, square_id):
    return HttpResponse(str(square_id))
