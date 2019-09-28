from django.shortcuts import render, HttpResponse
from .models.Player import Player
import csv
# Create your views here.


def LeaderBoard(request):
    if(request.GET.get('password') == "z12a34p"):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="leaderboards.csv"'

        writer = csv.writer(response)
        for player in Player.objects.all():
            writer.writerow([player.name, player.email])
        return response
    else:
        return HttpResponse("You are not authorized to see this page!")
