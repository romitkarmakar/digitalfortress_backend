from google.oauth2 import id_token
from django.core.exceptions import ObjectDoesNotExist
from google.auth.transport import requests
from django.contrib.auth.models import User
from rest_framework import viewsets, generics, authentication, permissions
from knox.models import AuthToken
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import permission_classes, APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.http import HttpResponse, JsonResponse
from quiz.models.Round import Round
from quiz.models.Player import Player
from quiz.models.Clue import Clue
import datetime
import json
import csv
import os
from django.utils import timezone
import urllib
from .serializers import CreateUserSerializer, RoundSerializer, PlayerSerializer
# Create your views here.


'''@APIView(['GET'])
def ge_Round(request):
    email = request.GET.get("email")
    if verifyUser(email) == 0:
        return JsonResponse({"status": 500})
    else:
        user = Player.objects.get(email=email)
        roundNo = user.score / 10 + 1
        try:
            round = Round.objects.get(round_number=roundNo)
        except:
            return JsonResponse({"status": 404})
        return JsonResponse({"status": 200, "question": round.question})


@APIView(['POST'])
def check_ound(request):
    email = request.GET.get("email")
    if verifyUser(email) == 0:
        return JsonResponse({"status": 500})
    else:
        user = Player.objects.get(email=email)
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
            return JsonResponse({"status": 500})
@APIView(['GET'])
def getClues(request):
    response = []
    email = request.GET.get("email")
    if verifyUser(email) == 0:
        return JsonResponse({"status": 500})
    else:
        user = Player.objects.get(email=email)
        roundNo = user.score / 10 + 1
        round = Round.objects.get(round_number=roundNo)
        clues = Clue.objects.filter(round=round)
        for clue in clues:
            if user.checkClue(clue.id):
                response.append(
                    {
                        "id": clue.id,
                        "question": clue.question,
                        "position": clue.getPosition(),
                        "isSolved": 1,
                    }
                )
            else:
                response.append(
                    {"id": clue.id, "question": clue.question, "isSolved": 0}
                )
        return JsonResponse(response, safe=False)

@APIView(['POST'])
def checkClue(request):
    email = request.GET.get("email")
    if verifyUser(email) == 0:
        return JsonResponse({"status": 500})
    else:
        user = Player.objects.get(email=email)
        roundNo = user.score / 10 + 1
        round = Round.objects.get(round_number=roundNo)
        clue = Clue.objects.get(pk=request.GET.get("clue"))
        if clue.checkAnswer(request.GET.get("answer")):
            user.putClues(clue.pk)
            user.save()
            return JsonResponse({"isTrue": 1, "position": clue.getPosition()})
        else:
            return JsonResponse({"isTrue": 0})
'''


def LeaderBoard(request):
    if request.GET.get("password") == os.environ.get('DOWNLOAD'):
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = 'attachment; filename="leaderboards.csv"'
        writer = csv.writer(response)
        for player in Player.objects.order_by("-score", "submit_time"):
            writer.writerow([player.name, player.email])
        return response
    else:
        return HttpResponse("You are not authorized to see this page!")


def verifyGoogleToken(token):
    CLIENT_ID = os.environ.get('CLIENT_ID')
    idinfo = id_token.verify_oauth2_token(
        token, requests.Request(), CLIENT_ID)

    if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
        raise ValueError('Wrong issuer.')

    return {
        "email": idinfo['email'],
        "username": idinfo['name'],
        "image": idinfo['picture']
    }


def verifyFacebookToken(token):
    APP_SECRET = os.environ.get('APP_SECRET')
    APP_ID = os.environ.get('APP_ID')

    appLink = 'https://graph.facebook.com/oauth/access_token?client_id={}&client_secret={}&grant_type=client_credentials'.format(
        APP_ID, APP_SECRET)
    appToken = requests.get(appLink).json()['access_token']
    link = 'https://graph.facebook.com/debug_token?input_token={}&access_token={}'.format(
        token, appToken)

    try:
        userId = requests.get(link).json()['data']['user_id']
    except (ValueError, KeyError, TypeError) as error:
        return Response({"error": error})
    return userId


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


def verifyUser(email):
    try:
        Player.objects.get(email=email)
        return True
    except ObjectDoesNotExist:
        return False


@permission_classes([AllowAny, ])
class leaderboard(generics.GenericAPIView):
    def get(self, request, format=None):
        p = Player.objects.order_by("-score", "submit_time")
        current_rank = 1
        players_array = []
        for player in p:
            player.rank = current_rank
            players_array.append({
                "name": player.name,
                "rank": player.rank,
                "score": player.score,
                "image": player.image,
            })
            current_rank += 1
        return Response({"standings": players_array, "safe": False})


@permission_classes([AllowAny, ])
class Register(generics.GenericAPIView):
    serializer_class = CreateUserSerializer

    def post(self, request, *args, **kwargs):
        if request.data.get('type') == '1':
            res = verifyGoogleToken(request.data.get('accesstoken'))
        else:
            res = verifyFacebookToken(request.data.get('accesstoken'))
        if verifyUser(res['email']) == False:
            serializer = self.get_serializer(data=res)
            serializer.is_valid(raise_exception=True)
            user = serializer.save()
            player = Player.objects.create(
                name=res['username'], email=res['email'], image=res['image'])
            return Response({
                "user": serializer.data,
                "token": AuthToken.objects.create(user)[1],
                "status": 200
            })
        else:
            return Response({"message": "Email Already Registered!", "status": 402})


@permission_classes([AllowAny, ])
class Login(generics.GenericAPIView):
    serializer_class = PlayerSerializer

    def post(self, request, *args, **kwargs):
        if request.data.get('type') == '1':
            res = verifyGoogleToken(request.data.get('accesstoken'))
        else:
            res = verifyFacebookToken(request.data.get('accesstoken'))

        if verifyUser(res['email']) == True:
            '''serializer = self.get_serializer(data=res)
            serializer.is_valid(raise_exception=True)
            user = serializer.validated_data'''
            user = User.objects.get(username=res['username'])
            player = Player.objects.get(name=res['username'])
            serializer = self.get_serializer(player)
            return Response({
                "user": serializer.data,
                "token": AuthToken.objects.create(user)[1],
                "status": 200
            })
        else:
            return Response({
                "message": "Email is not registered!",
                "status": 404
            })


@permission_classes([IsAuthenticated, ])
class getRound(APIView):
    def get(self, request, format=None):
        player = Player.objects.get(name=request.data.get('username'))
        roundno = player.score/10 + 1
        try:
            curr_round = Round.objects.get(round_number=roundno)
            serializer = RoundSerializer(curr_round)
            centre = centrePoint(curr_round)
            return Response({"question": serializer.data, "centre": centre, "status": 200, "detail": 1})
        except:
            if roundno == len(Round.objects.all()):
                return Response({"message": "Finished!", "status": 404, "detail": 1})
        return Response({"data": None})


@permission_classes([IsAuthenticated])
class checkRound(APIView):
    def post(self, request, *args, **kwargs):
        try:
            player = Player.objects.get(name=request.data.get('username'))
            round = Round.objects.get(
                round_number=(player.score/10+1))
            if round.checkAnswer(request.data.get("answer")):
                player.score += 10
                player.submit_time = timezone.now()
                player.save()
                return Response({"status": 200, "detail": 1})
            else:
                return Response({"status": 500, "detail": 1})
        except Player.DoesNotExist or Round.DoesNotExist:
            return Response({"data": None, "status": 404, "detail": 1})


@permission_classes([IsAuthenticated])
class getClue(APIView):
    def get(self, request, format=None):
        try:
            player = Player.objects.get(name=request.data.get('username'))
            round = Round.objects.get(round_number=(player.score/10+1))
            response = []
            clues = Clue.objects.filter(round=round)
            for clue in clues:
                if player.checkClue(clue.id):
                    response.append({
                        "id": clue.id,
                        "question": clue.question,
                        "position": clue.getPosition(),
                        "solved": True
                    })
                else:
                    response.append(
                        {"id": clue.id, "question": clue.question, "solved": False}
                    )
            return Response({"clues": response, "status": 200, "detail": 1})
        except Player.DoesNotExist or Round.DoesNotExist:
            return Response({"data": None, "status": 404, "detail": 1})


@permission_classes([IsAuthenticated])
class putClue(APIView):
    def post(self, request, *args, **kwargs):
        try:
            player = Player.objects.get(name=request.data.get("username"))
            clue = Clue.objects.get(pk=int(request.data.get("clue")))
            if clue.checkAnswer(request.data.get("answer")):
                player.putClues(clue.pk)
                player.save()
                return Response({"status": 200, "position": clue.getPosition(), "detail": 1})
            else:
                return Response({"status": 500, "detail": 1})
        except Player.DoesNotExist:
            return ({"data": None, "status": 404})
