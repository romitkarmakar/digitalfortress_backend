from django.urls import path
from .controller import authentication
from django.conf import settings
from django.conf.urls.static import static
from .views import LeaderBoard, getClues, getRound, checkClue, checkRound, leaderboard

urlpatterns = [
    path('getRound', getRound, name='getQuestion'),
    path('getClues', getClues, name='getClues'),
    path('checkRound', checkRound, name='checkRound'),
    path('checkClue', checkClue, name='checkClue'),
    path('leaderboard', leaderboard, name='leaderboard'),
    path('register', authentication.register, name='register'),
    path('saveLeaderBoard', LeaderBoard, name="download"),
]

# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
