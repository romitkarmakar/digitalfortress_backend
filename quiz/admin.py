from django.contrib import admin
from .models.Round import Round
from .models.Player import Player
from .models.Clue import Clue

admin.site.register(Clue)
admin.site.register(Round)
admin.site.register(Player)
