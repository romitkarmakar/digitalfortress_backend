from django.http import HttpResponse, JsonResponse
from quiz.models.Round import Round
from quiz.models.Player import Player
from quiz.models.Clue import Clue
import datetime
import json
from quiz.controller.authentication import verifyUser
from django.utils import timezone
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from controller.authentication import verifyGoogleToken, verifyFacebookToken
import urllib


@csrf_exempt
@require_POST()
def getRound(request):
    access_token = request.POST.get("access_token")
    if(request.POST.get['type'] == '0'):
        res = verifyGoogleToken(access_token)
    else:
        res = verifyFacebookToken(access_token)

    if verifyUser(res['email']) == 0:
        return JsonResponse({"status": 401})
    else:
        user = Player.objects.get(email=res['email'])
        roundNo = user.score / 10 + 1
        try:
            round = Round.objects.get(round_number=roundNo)
        except:
            return JsonResponse({"status": 404})
        return JsonResponse({"status": 200, "question": round.question, "centre": centrePoint(roundNo)})


@csrf_exempt
@require_POST()
def checkRound(request):
    access_token = request.POST.get("access_token")
    if(request.POST.get['type'] == '0'):
        res = verifyGoogleToken(access_token)
    else:
        res = verifyFacebookToken(access_token)

    if verifyUser(res['email']) == 0:
        return JsonResponse({"status": 401})
    else:
        user = Player.objects.get(email=res['email'])
        roundNo = user.score / 10 + 1
        try:
            round = Round.objects.get(round_number=roundNo)
        except:
            return JsonResponse({"status": 404})
        if round.checkAnswer(request.GET.get("answer")):
            user.score += 10
            user.submit_time = timezone.now()
            user.save()
            return JsonResponse({"status": 200})
        else:
            return JsonResponse({"status": 401})


@csrf_exempt
@require_POST()
def getClues(request):
    response = []
    access_token = request.POST.get("access_token")
    if(request.POST.get['type'] == '0'):
        res = verifyGoogleToken(access_token)
    else:
        res = verifyFacebookToken(access_token)

    if verifyUser(res['email']) == 0:
        return JsonResponse({"status": 401})
    else:
        user = Player.objects.get(email=res['email'])
        roundNo = user.score / 10 + 1
        round = Round.objects.get(round_number=roundNo)
        clues = Clue.objects.filter(round=round)
        for clue in clues:
            if user.checkClue(clue.id):
                response.append(
                    {"id": clue.id, "question": clue.question,
                        "position": clue.getPosition(), 'isSolved': 1}
                )
            else:
                response.append(
                    {"id": clue.id, "question": clue.question, 'isSolved': 0}
                )
        return JsonResponse(response, safe=False)


@csrf_exempt
@require_POST()
def checkClue(request):
    access_token = request.POST.get("access_token")
    if(request.POST.get['type'] == '0'):
        res = verifyGoogleToken(access_token)
    else:
        res = verifyFacebookToken(access_token)

    if verifyUser(res['email']) == 0:
        return JsonResponse({"status": 401})
    else:
        user = Player.objects.get(email=res['email'])
        roundNo = user.score / 10 + 1
        round = Round.objects.get(round_number=roundNo)
        clue = Clue.objects.get(pk=request.GET.get("clue"))
        if clue.checkAnswer(request.GET.get("answer")):
            user.putClues(clue.pk)
            user.save()
            return JsonResponse({"isTrue": 1, "position": clue.getPosition()})
        else:
            return JsonResponse({"isTrue": 0})


def leaderboard(request):
    p = Player.objects.order_by("-score", "submit_time")
    current_rank = 1
    players_array = []
    for player in p:
        player.rank = current_rank
        players_array.append(
            {
                "name": player.name,
                "rank": player.rank,
                "score": player.score,
                "image": player.image,
            }
        )
        current_rank += 1
    return JsonResponse(players_array, safe=False)


def centrePoint(roundNo):
    clues = Clue.objects.filter(round=roundNo)
    x = 0.0
    y = 0.0
    count = 0
    for clue in clues:
        pos = clue.getPosition()
        x += pos[0]
        y += pos[1]
        count += 1
    centre = []
    centre.append(x/count)
    centre.append(y/count)
    return centre
