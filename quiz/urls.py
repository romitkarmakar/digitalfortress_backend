from django.urls import path
from .controller import question, authentication
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('getRound', question.getRound, name='getQuestion'),
    path('getClues', question.getClues, name='getClues'),
    path('checkRound', question.checkRound, name='checkRound'),
    path('checkClue', question.checkClue, name='checkClue'),
    path('leaderboard', question.leaderboard, name='leaderboard'),
    path('register', authentication.register, name='register'),
]

# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
     