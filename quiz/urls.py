from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import LeaderBoard, getClue, getRound, putClue, checkRound, leaderboard, Login, Register

urlpatterns = [
    path('leaderboard', leaderboard, name='leaderboard'),
    path('saveLeaderBoard', LeaderBoard, name="download"),
    path('getRound', getRound.as_view(), name='round'),
    path('checkRound', checkRound.as_view(), name="checkRound"),
    path('getClue', getClue.as_view(), name="clue"),
    path('checkClue', putClue.as_view(), name="checkClue"),
    path('auth/login', Login.as_view(), name="login"),
    path('auth/register', Register.as_view(), name="register"),
]

# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
