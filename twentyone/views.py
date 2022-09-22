from django.shortcuts import render

#import cards

# Create your views here.

def game(request):

    context = {'coins': 1000}
    return render(request, 'twentyone/game.html', context)
