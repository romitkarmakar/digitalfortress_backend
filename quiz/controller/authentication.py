from google.oauth2 import id_token
from google.auth.transport import requests
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, JsonResponse

from quiz.models.Player import Player


def verifyGoogleToken(token):
    CLIENT_ID = '1066270839928-ulo4qi9cai9liclom3ca7cjel1h248hj.apps.googleusercontent.com'
    idinfo = id_token.verify_oauth2_token(
        token, requests.Request(), CLIENT_ID)

    if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
        raise ValueError('Wrong issuer.')

    return {
        "email": idinfo['email'],
        "name": idinfo['name'],
        "image": idinfo['picture']
    }


def verifyFacebookToken(token):
    APP_SECRET = 'fdd185af07273c8269555b67295db4c7'
    APP_ID = '2749120435101395'

    appLink = 'https://graph.facebook.com/oauth/access_token?client_id={}&client_secret={}&grant_type=client_credentials'.format(
        APP_ID, APP_SECRET)
    appToken = requests.get(appLink).json()['access_token']
    link = 'https://graph.facebook.com/debug_token?input_token={}&access_token={}'.format(
        token, appToken)

    try:
        userId = requests.get(link).json()['data']['user_id']
    except (ValueError, KeyError, TypeError) as error:
        return error
    return userId


def register(request):
    if request.GET.get('type') == '1':
        res = verifyGoogleToken(request.GET.get('id_token'))
    else:
        res = verifyFacebookToken(request.GET.get('id_token'))

    if verifyUser(res['email']) == 0:
        player = Player(name=res['name'],
                        email=res['email'], image=res['image'])
        player.save()
        return JsonResponse({
            'status': "Email Registered Succesfully!!"
        })
    else:
        return JsonResponse({
            'status': 402,
            'message': "Email Already Registered!!",
        })


def verifyUser(email):
    try:
        Player.objects.get(email=email)
        return 1
    except ObjectDoesNotExist:
        return 0
